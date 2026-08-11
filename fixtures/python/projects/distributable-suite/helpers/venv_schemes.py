"""PKG-016 virtual environments and install schemes."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import sysconfig


def create_venv(path: pathlib.Path) -> list[str]:
    return [sys.executable, "-m", "venv", str(path)]


def inspect_venv(venv: pathlib.Path) -> dict[str, str]:
    bin_dir = "Scripts" if sys.platform == "win32" else "bin"
    exe = venv / bin_dir / "python"
    # Retrieve venv config without activation: run venv's python
    return {
        "prefix": str(venv),
        "executable": str(exe),
        "import_origin_via_venv": f"{exe} -c 'import suite_core; print(suite_core.__file__)'",
        "direct_checkout": f"{sys.executable} -c 'import suite_core; print(suite_core.__file__)'",
        "system_site_note": "venv with --system-site-packages exposes host site; default isolated",
        "activation_note": "activation is optional; PATH not required when invoking venv python directly",
        "scheme_prefix": sysconfig.get_path("purelib"),
        "venv_purelib": str(venv / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"),
        "non_portability": "venv is non-portable; contains absolute paths",
        "symlink_vs_copy": "venv may use symlinks or copies depending on --copies flag",
        "user_site": sysconfig.get_path("purelib", vars={"user": True}) if hasattr(sysconfig, "get_path") else "",
    }


def compare_prefixes_note() -> str:
    return "venv prefix differs from base prefix; import origin moves into venv site-packages"
