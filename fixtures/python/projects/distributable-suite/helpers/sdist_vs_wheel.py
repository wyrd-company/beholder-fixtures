"""PKG-004 sdist versus wheel contents, built offline from the vendored wheelhouse."""

from __future__ import annotations

import hashlib
import pathlib
import subprocess
import tarfile
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).parents[1]
WHEELHOUSE = ROOT / "wheelhouse"
CORE = ROOT / "distributions" / "suite_core"

# uv build resolves the pinned setuptools backend from the vendored wheelhouse
# with no network access, so both the source distribution and the
# wheel-from-source-distribution build succeed offline from a clean cache.
_OFFLINE_INDEX = ["--offline", "--no-index", "--find-links", str(WHEELHOUSE)]


def build_only_path() -> str:
    """build_only_sdist.txt is included via MANIFEST.in so the sdist has it, the wheel does not."""
    return "distributions/suite_core/build_only_sdist.txt"


def generated_installed_path() -> str:
    """_generated_version.py is installed source, present in both sdist and wheel."""
    return "suite_core/_generated_version.py"


def build_sdist_offline(out_dir: pathlib.Path) -> pathlib.Path | None:
    """Build the source distribution offline via the vendored backend."""
    out_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["uv", "build", "--sdist", *_OFFLINE_INDEX, "--out-dir", str(out_dir), str(CORE)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    candidates = sorted(out_dir.glob("*.tar.gz"))
    return candidates[-1] if candidates else None


def build_wheel_from_sdist_offline(sdist: pathlib.Path, out_dir: pathlib.Path) -> pathlib.Path | None:
    """Build a wheel from the source distribution offline via the vendored backend."""
    out_dir.mkdir(parents=True, exist_ok=True)
    before = set(out_dir.glob("*.whl"))
    result = subprocess.run(
        ["uv", "build", "--wheel", *_OFFLINE_INDEX, "--out-dir", str(out_dir), str(sdist)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    new = sorted(set(out_dir.glob("*.whl")) - before)
    return new[0] if new else None


def sdist_members(sdist: pathlib.Path) -> list[str]:
    with tarfile.open(sdist) as tf:
        return tf.getnames()


def wheel_members(wheel: pathlib.Path) -> list[str]:
    with zipfile.ZipFile(wheel) as zf:
        return zf.namelist()


def sdist_contains_build_only(sdist: pathlib.Path) -> bool:
    return any(name.endswith("build_only_sdist.txt") for name in sdist_members(sdist))


def wheel_omits_build_only(wheel: pathlib.Path) -> bool:
    return not any(name.endswith("build_only_sdist.txt") for name in wheel_members(wheel))


def wheel_contains_generated(wheel: pathlib.Path) -> bool:
    return any(name.endswith("suite_core/_generated_version.py") for name in wheel_members(wheel))


def _wheel_payload_hashes(wheel: pathlib.Path) -> list[tuple[str, str]]:
    """Sorted (name, sha256) of installed source files.

    Excludes ``.dist-info`` metadata and ``__pycache__``/``.pyc`` byte-code, which
    are build-environment artifacts (a tree that was byte-compiled ships stale
    ``.pyc`` that a freshly unpacked sdist does not) rather than installed source.
    """
    with zipfile.ZipFile(wheel) as zf:
        return sorted(
            (name, hashlib.sha256(zf.read(name)).hexdigest())
            for name in zf.namelist()
            if ".dist-info/" not in name and "__pycache__/" not in name and not name.endswith(".pyc")
        )


def wheel_from_tree_matches_wheel_from_sdist(wheel_tree: pathlib.Path, wheel_sdist: pathlib.Path) -> bool:
    """Installed payloads of the two wheels are byte-equivalent (metadata aside)."""
    return _wheel_payload_hashes(wheel_tree) == _wheel_payload_hashes(wheel_sdist)


def demonstrate() -> dict[str, bool]:
    """Build sdist and wheel-from-sdist offline and verify the content contract."""
    with tempfile.TemporaryDirectory() as td:
        out = pathlib.Path(td)
        sdist = build_sdist_offline(out)
        if sdist is None:
            return {"sdist_built": False}
        wheel_from_sdist = build_wheel_from_sdist_offline(sdist, out)
        tree_wheel = subprocess.run(
            ["uv", "build", "--wheel", *_OFFLINE_INDEX, "--out-dir", str(out / "tree"), str(CORE)],
            capture_output=True, text=True,
        )
        tree_wheels = sorted((out / "tree").glob("*.whl")) if tree_wheel.returncode == 0 else []
        result = {
            "sdist_built": True,
            "wheel_from_sdist_built": wheel_from_sdist is not None,
            "sdist_has_build_only": sdist_contains_build_only(sdist),
            "wheel_omits_build_only": wheel_from_sdist is not None and wheel_omits_build_only(wheel_from_sdist),
            "wheel_has_generated": wheel_from_sdist is not None and wheel_contains_generated(wheel_from_sdist),
        }
        if wheel_from_sdist is not None and tree_wheels:
            result["tree_matches_sdist_payload"] = wheel_from_tree_matches_wheel_from_sdist(tree_wheels[0], wheel_from_sdist)
        return result


def missing_input_note() -> str:
    return "a missing input file listed in MANIFEST.in would be omitted from the sdist"
