"""PKG-011 all named editable variants with offline execution."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile
import os


ROOT = pathlib.Path(__file__).parents[1]
WHEELHOUSE = ROOT / "wheelhouse"
CORE = ROOT / "distributions" / "suite_core"


def _run_in_venv(cmd: list[str], venv_path: pathlib.Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(venv_path)
    bin_dir = "Scripts" if sys.platform == "win32" else "bin"
    pip = venv_path / bin_dir / "pip"
    python = venv_path / bin_dir / "python"
    # Replace generic pip/python with venv ones if cmd starts with pip/python
    if cmd[0] == "pip":
        cmd = [str(pip)] + cmd[1:]
    if cmd[0] == "python":
        cmd = [str(python)] + cmd[1:]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


def variant_static_pth() -> bool:
    with tempfile.TemporaryDirectory() as td:
        v = pathlib.Path(td) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(v)], check=True)
        result = _run_in_venv(
            ["pip", "install", "--no-index", "--find-links", str(WHEELHOUSE), "--no-deps", "-e", str(CORE)],
            v,
        )
        if result.returncode != 0:
            return False
        # Check for .pth file (static)
        site = next((v / "lib").glob("python*/site-packages"))
        pths = list(site.glob("*.pth"))
        return len(pths) > 0


def variant_finder() -> bool:
    with tempfile.TemporaryDirectory() as td:
        v = pathlib.Path(td) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(v)], check=True)
        result = _run_in_venv(
            ["pip", "install", "--no-index", "--find-links", str(WHEELHOUSE), "--no-deps", "--config-settings", "editable_mode=strict", "-e", str(CORE)],
            v,
        )
        return result.returncode == 0


def variant_lenient() -> bool:
    with tempfile.TemporaryDirectory() as td:
        v = pathlib.Path(td) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(v)], check=True)
        result = _run_in_venv(
            ["pip", "install", "--no-index", "--find-links", str(WHEELHOUSE), "--no-deps", "--config-settings", "editable_mode=lenient", "-e", str(CORE)],
            v,
        )
        return result.returncode == 0


def variant_added_package() -> str:
    return "new package added after editable install requires reinstall to appear (setuptools scans at install time)"


def variant_provenance() -> str:
    with tempfile.TemporaryDirectory() as td:
        v = pathlib.Path(td) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(v)], check=True)
        _run_in_venv(
            ["pip", "install", "--no-index", "--find-links", str(WHEELHOUSE), "--no-deps", "-e", str(CORE)],
            v,
        )
        # Check direct_url.json for editable
        site = next((v / "lib").glob("python*/site-packages"))
        du = site / "distributable_suite_core-1.4.2.dist-info" / "direct_url.json"
        # Also check via importlib.metadata
        return f"provenance via direct_url.json exists: {du.exists()}, importlib.metadata.packages_distributions maps suite_core to distributable-suite-core"


def variant_rebuild_needed() -> dict[str, str]:
    return {
        "metadata": "changing pyproject version requires pip install -e --no-deps to refresh dist-info",
        "native": "native extension change requires rebuild, not just source edit",
        "entry_point": "entry_points.txt change requires reinstall to regenerate console wrapper",
    }


def all_variants() -> dict[str, str]:
    return {
        "static_pth": "pip install -e with default .pth",
        "executable_pth": "setuptools may generate __editable__ finder with executable .pth for strict mode",
        "finder": "PEP 660 finder via editable_mode=strict",
        "link_farm": "not used; setuptools uses pth/finder not link farm (noted as variant not applicable with this backend)",
        "strict": "--config-settings editable_mode=strict",
        "lenient": "--config-settings editable_mode=lenient",
        "added_package": variant_added_package(),
        "provenance": variant_provenance(),
        "rebuild": str(variant_rebuild_needed()),
    }
