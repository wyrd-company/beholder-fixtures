"""PKG-016 virtual environments and install schemes with isolated execution."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import sysconfig
import tempfile

ROOT = pathlib.Path(__file__).parents[1]
WHEELHOUSE = ROOT / "wheelhouse"
CORE = ROOT / "distributions" / "suite_core"
_BIN = "Scripts" if sys.platform == "win32" else "bin"


def create_venv(path: pathlib.Path) -> list[str]:
    return [sys.executable, "-m", "venv", str(path)]


def create_venv_variants(base: pathlib.Path) -> dict[str, pathlib.Path]:
    """Create default, system-site, and copies venv variants."""
    variants: dict[str, pathlib.Path] = {}
    for name, extra in [("default", []), ("system_site", ["--system-site-packages"]), ("copies", ["--copies"])]:
        target = base / name
        subprocess.run([sys.executable, "-m", "venv", str(target), *extra], check=True)
        variants[name] = target
    return variants


def inspect_venv(venv: pathlib.Path) -> dict[str, str]:
    exe = venv / _BIN / "python"
    result = subprocess.run(
        [str(exe), "-c", "import sys, sysconfig; print(sys.prefix); print(sys.executable); print(sysconfig.get_path('purelib'))"],
        capture_output=True, text=True,
    )
    lines = result.stdout.strip().splitlines()
    return {
        "prefix": lines[0] if lines else str(venv),
        "executable": lines[1] if len(lines) > 1 else str(exe),
        "venv_purelib": lines[2] if len(lines) > 2 else "",
        "base_purelib": sysconfig.get_path("purelib"),
        "system_site_note": "venv with --system-site-packages exposes host site; default is isolated",
        "activation_note": "activation is optional; invoking the venv python directly needs no PATH change",
        "non_portability": "venv is non-portable; it records absolute paths",
        "symlink_vs_copy": "the copies variant uses --copies; the default uses symlinks where possible",
    }


def user_site_purelib(userbase: pathlib.Path) -> str:
    """Resolve the user-site purelib for a given userbase.

    Uses the ``posix_user`` install scheme so the path lands under ``userbase``
    and is distinct from the base ``purelib`` -- unlike ``vars={"user": True}``,
    which is not a scheme selector and collapses to the base purelib.
    """
    return sysconfig.get_path("purelib", "posix_user", vars={"userbase": str(userbase)})


def install_scheme_target() -> bool:
    """Execute a --target install scheme offline and import from the target dir."""
    with tempfile.TemporaryDirectory() as td:
        target = pathlib.Path(td) / "tgt"
        install = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--no-index", "--find-links", str(WHEELHOUSE), "--no-deps", "--target", str(target), str(CORE)],
            capture_output=True, text=True,
        )
        if install.returncode != 0:
            return False
        check = subprocess.run(
            [sys.executable, "-c", "import suite_core; print(suite_core.__file__)"],
            capture_output=True, text=True, env={"PYTHONPATH": str(target), "PATH": "/usr/bin:/bin"},
        )
        return check.returncode == 0 and str(target) in check.stdout


def install_scheme_prefix() -> bool:
    """Execute a --prefix install scheme offline and confirm the install location."""
    with tempfile.TemporaryDirectory() as td:
        prefix = pathlib.Path(td) / "pfx"
        install = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--no-index", "--find-links", str(WHEELHOUSE), "--no-deps", "--prefix", str(prefix), str(CORE)],
            capture_output=True, text=True,
        )
        if install.returncode != 0:
            return False
        return any(prefix.rglob("suite_core/__init__.py"))


def user_site_scheme_distinct() -> bool:
    """The user-site purelib resolves under the userbase, distinct from base purelib."""
    with tempfile.TemporaryDirectory() as td:
        user_path = pathlib.Path(user_site_purelib(pathlib.Path(td)))
        return str(td) in str(user_path) and str(user_path) != sysconfig.get_path("purelib")


def user_site_override_note() -> str:
    return (
        "the reviewed base interpreter is externally managed (PEP 668), so a host "
        "user-site install is refused without --break-system-packages; the executed "
        "scheme contrasts use --target and --prefix, which need no host override"
    )


def activation_independent_demo() -> bool:
    """Import works without activation, via the venv python path, after an offline install."""
    with tempfile.TemporaryDirectory() as td:
        venv = pathlib.Path(td) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
        exe = venv / _BIN / "python"
        subprocess.run(
            [str(exe), "-m", "pip", "install", "--no-index", "--find-links", str(WHEELHOUSE), "--no-deps", str(CORE)],
            capture_output=True,
        )
        result = subprocess.run([str(exe), "-c", "import suite_core; print(suite_core.__version__)"], capture_output=True, text=True)
        return result.returncode == 0
