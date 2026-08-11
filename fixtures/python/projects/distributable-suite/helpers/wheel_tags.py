"""PKG-010 wheel compatibility tags inspection."""

from __future__ import annotations

import pathlib
import zipfile
import sysconfig


def pure_tag() -> str:
    return "py3-none-any"


def native_tag() -> str:
    # CPython + ABI + platform on this host
    impl = f"cp{sysconfig.get_python_version().replace('.', '')}"
    abi = impl
    plat = "linux_x86_64"
    return f"{impl}-{abi}-{plat}"


def abi3_tag() -> str:
    # Stable ABI would be cp310-abi3-linux_x86_64 etc
    return "cp310-abi3-linux_x86_64"


def manylinux_tag() -> str:
    return "cp314-cp314-manylinux_2_34_x86_64"


def inspect_wheel_tags(wheel: pathlib.Path) -> list[str]:
    if not wheel.exists():
        return [pure_tag(), native_tag(), abi3_tag()]
    with zipfile.ZipFile(wheel) as zf:
        wheel_info = [n for n in zf.namelist() if n.endswith("WHEEL")]
        if wheel_info:
            return zf.read(wheel_info[0]).decode().splitlines()
    return []


def invalid_retag_note() -> str:
    return "invalid retag (e.g. marking pure as platform) would cause installer mismatch"
