"""PKG-010 wheel compatibility tags inspection.

Reads the actual ``Tag:`` lines from a built wheel's ``WHEEL`` metadata rather
than asserting a tag string. ``distributable-suite-native`` builds a full-ABI
``cpXY-cpXY-<platform>`` wheel; ``distributable-suite-native-abi3`` builds a
stable-ABI ``cpXY-abi3-<platform>`` wheel; other distributions build pure
``py3-none-any`` wheels.
"""

from __future__ import annotations

import pathlib
import zipfile


def pure_tag() -> str:
    return "py3-none-any"


def abi3_tag() -> str:
    # Stable-ABI wheels are tagged against the limited-API floor (cp310 here).
    return "cp310-abi3-linux_x86_64"


def manylinux_tag() -> str:
    return "cp314-cp314-manylinux_2_34_x86_64"


def read_wheel_tags(wheel: pathlib.Path) -> list[str]:
    """Return the ``Tag:`` values recorded in a wheel's WHEEL metadata."""
    with zipfile.ZipFile(wheel) as zf:
        wheel_meta = next((n for n in zf.namelist() if n.endswith(".dist-info/WHEEL")), None)
        if wheel_meta is None:
            return []
        return [
            line.split(":", 1)[1].strip()
            for line in zf.read(wheel_meta).decode().splitlines()
            if line.startswith("Tag:")
        ]


def inspect_wheel_tags(wheel: pathlib.Path) -> list[str]:
    """Return the full WHEEL metadata lines for a built wheel (empty if absent)."""
    if not wheel.exists():
        return []
    with zipfile.ZipFile(wheel) as zf:
        wheel_info = [n for n in zf.namelist() if n.endswith("WHEEL")]
        if wheel_info:
            return zf.read(wheel_info[0]).decode().splitlines()
    return []


def is_abi3_wheel(wheel: pathlib.Path) -> bool:
    """True when the wheel advertises a stable-ABI (abi3) tag."""
    return any("-abi3-" in tag for tag in read_wheel_tags(wheel))


def invalid_retag_note() -> str:
    return "invalid retag (e.g. marking pure as platform) would cause installer mismatch"
