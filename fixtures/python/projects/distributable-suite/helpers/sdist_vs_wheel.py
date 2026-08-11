"""PKG-004 sdist versus wheel contents."""

from __future__ import annotations

import pathlib
import tarfile
import zipfile

ROOT = pathlib.Path(__file__).parents[1]


def sdist_contains_build_only() -> str:
    """build_only_sdist.txt is included via MANIFEST.in so sdist has it, wheel does not."""
    return "distributions/suite_core/build_only_sdist.txt"


def wheel_contains_generated() -> str:
    """_generated_version.py is package data so both sdist and wheel contain it,
    but wheel's installed form is generated from generator input."""
    return "suite_core/_generated_version.py"


def inspect_sdist_and_wheel(sdist: pathlib.Path, wheel: pathlib.Path) -> dict:
    result: dict[str, list[str]] = {"sdist": [], "wheel": []}
    if sdist.exists():
        with tarfile.open(sdist) as tf:
            result["sdist"] = tf.getnames()[:10]
    if wheel.exists():
        with zipfile.ZipFile(wheel) as zf:
            result["wheel"] = zf.namelist()[:20]
    return result


def wheel_from_tree_vs_sdist_note() -> str:
    return "wheel-from-tree and wheel-from-sdist should contain equivalent payload; timestamps/order may differ"


def missing_input_note() -> str:
    return "missing input file would cause build to omit that resource"


def pure_vs_platform_tags() -> str:
    return "pure wheel: py3-none-any, platform wheel: cp314-cp314-linux_x86_64"
