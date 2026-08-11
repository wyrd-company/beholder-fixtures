"""PKG-016 virtual environments and install schemes."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import sysconfig


def create_venv(path: pathlib.Path) -> list[str]:
    return [sys.executable, "-m", "venv", str(path)]


def create_venv_variants(base: pathlib.Path) -> dict[str, pathlib.Path]:
    """Create default, system-site, and copies variants."""
    variants: dict[str, pathlib.Path] = {}
    for name, extra in [("default", []), ("system_site", ["--system-site-packages"]), ("copies", ["--copies"])]:
        p = base / name
        cmd = [sys.executable, "-m", "venv", str(p)] + extra
        subprocess.run(cmd, check=True)
        variants[name] = p
    return variants


def inspect_venv(venv: pathlib.Path) -> dict[str, str]:
    bin_dir = "Scripts" if sys.platform == "win32" else "bin"
    exe = venv / bin_dir / "python"
    result = subprocess.run([str(exe), "-c", "import sys, sysconfig; print(sys.prefix); print(sys.executable); print(sysconfig.get_path('purelib'))"], capture_output=True, text=True)
    lines = result.stdout.strip().splitlines()
    prefix = lines[0] if lines else str(venv)
    executable = lines[1] if len(lines) > 1 else str(exe)
    purelib = lines[2] if len(lines) > 2 else ""
    return {
        "prefix": prefix,
        "executable": executable,
        "import_origin_via_venv": f"{exe} -c 'import suite_core; print(suite_core.__file__)'",
        "direct_checkout": f"{sys.executable} -c 'import suite_core; print(suite_core.__file__)'",
        "system_site_note": "venv with --system-site-packages exposes host site; default isolated",
        "activation_note": "activation is optional; PATH not required when invoking venv python directly",
        "scheme_prefix": sysconfig.get_path("purelib"),
        "venv_purelib": purelib,
        "non_portability": "venv is non-portable; contains absolute paths",
        "symlink_vs_copy": "variant copies uses --copies; default uses symlinks where possible",
        "user_site": sysconfig.get_path("purelib", vars={"user": True}) if hasattr(sysconfig, "get_path") else "",
    }


def activation_independent_demo() -> bool:
    """Show import works without activation via venv python path."""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        v = pathlib.Path(td) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(v)], check=True)
        bin_dir = "Scripts" if sys.platform == "win32" else "bin"
        exe = v / bin_dir / "python"
        # Install core offline without activation
        root = pathlib.Path(__file__).parents[1]
        subprocess.run([str(exe), "-m", "pip", "install", "--no-index", "--find-links", str(root / "wheelhouse"), "--no-deps", str(root / "distributions" / "suite_core")], capture_output=True)
        result = subprocess.run([str(exe), "-c", "import suite_core; print(suite_core.__version__)"], capture_output=True, text=True)
        return result.returncode == 0


def compare_prefixes_note() -> str:
    return "venv prefix differs from base prefix; import origin moves into venv site-packages"
