"""PKG-015 reproducible and environment-sensitive builds, built offline."""

from __future__ import annotations

import hashlib
import os
import pathlib
import subprocess
import tarfile
import tempfile

ROOT = pathlib.Path(__file__).parents[1]
WHEELHOUSE = ROOT / "wheelhouse"
CORE = ROOT / "distributions" / "suite_core"

# Both builds resolve the pinned setuptools backend from the vendored wheelhouse
# with no network access.
_OFFLINE_INDEX = ["--offline", "--no-index", "--find-links", str(WHEELHOUSE)]

# Two builds from equivalent normalized inputs produce equivalent artifacts once
# timestamps are clamped with SOURCE_DATE_EPOCH and the file order is sorted.
NORMALIZED_INPUTS = [
    "distributions/suite_core/suite_core/_generated_version.py",
    "distributions/suite_core/pyproject.toml",
]

COUNTERCASE = "SOURCE_DATE_EPOCH=0 versus 315532800 yields different mtimes in the sdist tar header"


def _build_sdist(out_dir: pathlib.Path, epoch: str) -> pathlib.Path | None:
    out_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = epoch
    result = subprocess.run(
        ["uv", "build", "--sdist", *_OFFLINE_INDEX, "--out-dir", str(out_dir), str(CORE)],
        env=env, capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    tarballs = sorted(out_dir.glob("*.tar.gz"))
    return tarballs[-1] if tarballs else None


def two_equivalent_builds() -> tuple[bool, str]:
    """Build the sdist twice with the same SOURCE_DATE_EPOCH; payloads must match."""
    with tempfile.TemporaryDirectory() as td:
        s1 = _build_sdist(pathlib.Path(td) / "out1", "315532800")
        s2 = _build_sdist(pathlib.Path(td) / "out2", "315532800")
        if s1 is None or s2 is None:
            return False, "offline sdist build failed"
        equal = compare_artifacts(s1, s2)
        return equal, f"{s1.name} vs {s2.name} payload equal={equal}"


def countercase_build() -> tuple[bool, str]:
    """Countercase: a different SOURCE_DATE_EPOCH yields a different tar mtime."""
    with tempfile.TemporaryDirectory() as td:
        s1 = _build_sdist(pathlib.Path(td) / "out1", "0")
        s2 = _build_sdist(pathlib.Path(td) / "out2", "315532800")
        if s1 is None or s2 is None:
            return False, "offline sdist build failed"
        with tarfile.open(s1) as tf:
            m1 = tf.getmembers()[0].mtime
        with tarfile.open(s2) as tf:
            m2 = tf.getmembers()[0].mtime
        return m1 != m2, f"mtime {m1} vs {m2} differ"


def compare_artifacts(artifact_a: pathlib.Path, artifact_b: pathlib.Path) -> bool:
    """Compare two tarballs by sorted member name and content hash, ignoring order."""
    def tar_hashes(path: pathlib.Path) -> list[tuple[str, str]]:
        with tarfile.open(path) as tf:
            return sorted(
                (m.name, hashlib.sha256(tf.extractfile(m).read()).hexdigest())
                for m in tf.getmembers() if m.isfile()
            )

    try:
        return tar_hashes(artifact_a) == tar_hashes(artifact_b)
    except Exception:
        return False


def environment_factors() -> list[str]:
    return ["time (SOURCE_DATE_EPOCH)", "locale", "file order", "paths", "compiler", "generated version drift"]
