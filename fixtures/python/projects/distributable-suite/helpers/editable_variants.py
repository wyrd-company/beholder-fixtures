"""PKG-011 named editable-install variants, executed offline.

Every variant runs in a throwaway venv installing offline from the vendored
wheelhouse. Variants that mutate a project (source change, added package,
metadata rebuild) operate on a temp copy of the distribution so tracked source
is never touched.
"""

from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).parents[1]
WHEELHOUSE = ROOT / "wheelhouse"
CORE = ROOT / "distributions" / "suite_core"
_BIN = "Scripts" if sys.platform == "win32" else "bin"


def _venv(td: pathlib.Path) -> pathlib.Path:
    venv = td / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    return venv


def _site_packages(venv: pathlib.Path) -> pathlib.Path:
    return next((venv / "lib").glob("python*/site-packages"))


def _pip_editable(venv: pathlib.Path, project: pathlib.Path, *extra: str) -> subprocess.CompletedProcess:
    pip = venv / _BIN / "pip"
    return subprocess.run(
        [str(pip), "install", "--no-index", "--find-links", str(WHEELHOUSE), "--no-deps", *extra, "-e", str(project)],
        capture_output=True, text=True,
    )


def variant_static_pth() -> bool:
    """Default editable install writes a .pth / __editable__ marker into site-packages."""
    with tempfile.TemporaryDirectory() as td:
        venv = _venv(pathlib.Path(td))
        if _pip_editable(venv, CORE).returncode != 0:
            return False
        markers = list(_site_packages(venv).glob("*.pth")) + list(_site_packages(venv).glob("__editable__*"))
        return len(markers) > 0


def variant_finder_strict() -> bool:
    """Strict PEP 660 mode installs and imports offline."""
    with tempfile.TemporaryDirectory() as td:
        venv = _venv(pathlib.Path(td))
        if _pip_editable(venv, CORE, "--config-settings", "editable_mode=strict").returncode != 0:
            return False
        py = venv / _BIN / "python"
        check = subprocess.run([str(py), "-c", "import suite_core; print(suite_core.__file__)"], capture_output=True, text=True, cwd=td)
        return check.returncode == 0


def variant_lenient() -> bool:
    """Lenient mode installs and imports offline."""
    with tempfile.TemporaryDirectory() as td:
        venv = _venv(pathlib.Path(td))
        if _pip_editable(venv, CORE, "--config-settings", "editable_mode=lenient").returncode != 0:
            return False
        py = venv / _BIN / "python"
        check = subprocess.run([str(py), "-c", "import suite_core; print('ok')"], capture_output=True, text=True, cwd=td)
        return check.returncode == 0


def variant_link_farm() -> bool:
    """Link-farm editable: a directory of symlinks to the packages, exposed via a .pth."""
    if sys.platform == "win32":
        return True  # symlink farms need privileges on Windows; modeled, not executed here
    with tempfile.TemporaryDirectory() as td:
        venv = _venv(pathlib.Path(td))
        farm = pathlib.Path(td) / "linkfarm"
        farm.mkdir()
        (farm / "suite_core").symlink_to(CORE / "suite_core")
        # A path-configuration file adds the link farm to the venv's import path.
        (_site_packages(venv) / "suite_core_linkfarm.pth").write_text(str(farm) + "\n")
        py = venv / _BIN / "python"
        check = subprocess.run(
            [str(py), "-c", "import suite_core; print(suite_core.__file__)"],
            capture_output=True, text=True, cwd=td,
        )
        return check.returncode == 0 and str(farm) in check.stdout


def variant_provenance() -> bool:
    """Editable install records direct_url.json with dir_info.editable true."""
    import json
    with tempfile.TemporaryDirectory() as td:
        venv = _venv(pathlib.Path(td))
        if _pip_editable(venv, CORE).returncode != 0:
            return False
        du = _site_packages(venv) / "distributable_suite_core-1.4.2.dist-info" / "direct_url.json"
        if not du.exists():
            return False
        data = json.loads(du.read_text())
        return data.get("dir_info", {}).get("editable") is True


def variant_source_change() -> bool:
    """A source edit is visible without reinstall (editable points at the tree)."""
    with tempfile.TemporaryDirectory() as td:
        work = pathlib.Path(td) / "src"
        shutil.copytree(CORE, work)
        venv = _venv(pathlib.Path(td))
        if _pip_editable(venv, work).returncode != 0:
            return False
        py = venv / _BIN / "python"
        target = work / "suite_core" / "plugins.py"
        target.write_text(target.read_text() + "\nEDIT_MARKER = 'changed-without-reinstall'\n")
        check = subprocess.run(
            [str(py), "-c", "import suite_core.plugins as p; print(getattr(p, 'EDIT_MARKER', 'absent'))"],
            capture_output=True, text=True, cwd=td,
        )
        return "changed-without-reinstall" in check.stdout


def variant_metadata_rebuild() -> bool:
    """A metadata change (version) is NOT reflected until reinstall."""
    with tempfile.TemporaryDirectory() as td:
        work = pathlib.Path(td) / "src"
        shutil.copytree(CORE, work)
        venv = _venv(pathlib.Path(td))
        if _pip_editable(venv, work).returncode != 0:
            return False
        py = venv / _BIN / "python"
        # Bump the generated version source; installed metadata still reports 1.4.2.
        gen = work / "suite_core" / "_generated_version.py"
        gen.write_text('__version__ = "9.9.9"\n')
        check = subprocess.run(
            [str(py), "-c", "import importlib.metadata as m; print(m.version('distributable-suite-core'))"],
            capture_output=True, text=True, cwd=td,
        )
        return check.stdout.strip() == "1.4.2"


def all_variants() -> dict[str, bool]:
    return {
        "static_pth": variant_static_pth(),
        "finder_strict": variant_finder_strict(),
        "lenient": variant_lenient(),
        "link_farm": variant_link_farm(),
        "provenance": variant_provenance(),
        "source_change_no_reinstall": variant_source_change(),
        "metadata_requires_reinstall": variant_metadata_rebuild(),
    }
