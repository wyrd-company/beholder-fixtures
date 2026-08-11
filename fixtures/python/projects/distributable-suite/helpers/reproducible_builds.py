"""PKG-015 reproducible and environment-sensitive builds."""

from __future__ import annotations

import pathlib

# Two builds from equivalent normalized inputs produce equivalent artifacts.
# Normalization: sorted file lists, clamped timestamps (SOURCE_DATE_EPOCH),
# deterministic file order via `sort` in archive creation.
# Actual builds via uv build --sdist with SOURCE_DATE_EPOCH=315532800.

NORMALIZED_INPUTS = [
    "distributions/suite_core/suite_core/_generated_version.py",
    "distributions/suite_core/pyproject.toml",
]

COUNTERCASE = "A build with SOURCE_DATE_EPOCH=0 vs 315532800 produces different timestamps in tar header (demonstrated via two sdist builds)"


def two_equivalent_builds() -> tuple[bool, str]:
    """Build sdist twice with same SOURCE_DATE_EPOCH and compare payload hashes."""
    import subprocess, hashlib, tarfile, tempfile, pathlib, os
    root = pathlib.Path(__file__).parents[1]
    with tempfile.TemporaryDirectory() as td:
        out1 = pathlib.Path(td) / "out1"
        out2 = pathlib.Path(td) / "out2"
        out1.mkdir(); out2.mkdir()
        env = os.environ.copy()
        env["SOURCE_DATE_EPOCH"] = "315532800"
        cmd1 = ["uv", "build", "--sdist", "--out-dir", str(out1), str(root / "distributions" / "suite_core")]
        r1 = subprocess.run(cmd1, env=env, capture_output=True, text=True)
        cmd2 = ["uv", "build", "--sdist", "--out-dir", str(out2), str(root / "distributions" / "suite_core")]
        r2 = subprocess.run(cmd2, env=env, capture_output=True, text=True)
        if r1.returncode != 0 or r2.returncode != 0:
            return False, f"build failed {r1.stderr[:200]}"
        s1 = next(out1.glob("*.tar.gz"))
        s2 = next(out2.glob("*.tar.gz"))
        return compare_artifacts(s1, s2), f"{s1.name} vs {s2.name} payload equal"


def countercase_build() -> tuple[bool, str]:
    """Countercase: different SOURCE_DATE_EPOCH yields different tar mtime."""
    import subprocess, tarfile, tempfile, pathlib, os
    root = pathlib.Path(__file__).parents[1]
    with tempfile.TemporaryDirectory() as td:
        out1 = pathlib.Path(td) / "out1"
        out2 = pathlib.Path(td) / "out2"
        out1.mkdir(); out2.mkdir()
        env1 = os.environ.copy(); env1["SOURCE_DATE_EPOCH"] = "0"
        env2 = os.environ.copy(); env2["SOURCE_DATE_EPOCH"] = "315532800"
        subprocess.run(["uv", "build", "--sdist", "--out-dir", str(out1), str(root / "distributions" / "suite_core")], env=env1, capture_output=True)
        subprocess.run(["uv", "build", "--sdist", "--out-dir", str(out2), str(root / "distributions" / "suite_core")], env=env2, capture_output=True)
        s1 = next(out1.glob("*.tar.gz"))
        s2 = next(out2.glob("*.tar.gz"))
        with tarfile.open(s1) as tf:
            m1 = tf.getmembers()[0].mtime
        with tarfile.open(s2) as tf:
            m2 = tf.getmembers()[0].mtime
        return m1 != m2, f"mtime {m1} vs {m2} differ"


def compare_artifacts(artifact_a: pathlib.Path, artifact_b: pathlib.Path) -> bool:
    """Compare ignoring timestamps: compare sorted namelist and file hashes."""
    import tarfile
    import hashlib

    def tar_hashes(p: pathlib.Path):
        with tarfile.open(p) as tf:
            return sorted((m.name, hashlib.sha256(tf.extractfile(m).read()).hexdigest()) for m in tf.getmembers() if m.isfile())

    try:
        return tar_hashes(artifact_a) == tar_hashes(artifact_b)
    except Exception:
        return False


def countercase_documentation() -> str:
    return (
        "Countercase: building sdist with mtime 2020-01-01 vs 2026-01-01 produces different tar headers; "
        "reproducible builds require SOURCE_DATE_EPOCH and sorted order"
    )


def environment_factors() -> list[str]:
    return ["time (SOURCE_DATE_EPOCH)", "locale", "file order", "paths", "compiler", "generated version drift"]
