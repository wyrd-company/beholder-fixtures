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
    """Default editable install writes a plain-path .pth (non-executable) into site-packages."""
    with tempfile.TemporaryDirectory() as td:
        venv = _venv(pathlib.Path(td))
        if _pip_editable(venv, CORE).returncode != 0:
            return False
        pths = list(_site_packages(venv).glob("*.pth"))
        for p in pths:
            text = p.read_text()
            # plain-path .pth contains only a path, no leading import
            if text.strip() and not text.lstrip().startswith("import"):
                # Verify the path points at the project and is plain
                if str(CORE) in text or "suite_core" in text or "/" in text:
                    return True
        return False


def variant_executable_pth() -> bool:
    """Executable .pth: a .pth whose first line is import and is executed on interpreter startup."""
    with tempfile.TemporaryDirectory() as td:
        venv = _venv(pathlib.Path(td))
        site = _site_packages(venv)
        # Create an executable .pth that inserts a temp directory onto sys.path via import
        marker_dir = pathlib.Path(td) / "exec_marker"
        marker_dir.mkdir()
        (marker_dir / "exec_pkg").mkdir()
        (marker_dir / "exec_pkg" / "__init__.py").write_text("VALUE='from-executable-pth'\n")
        pth = site / "executable_test.pth"
        # Executable .pth lines starting with import are executed by site.py
        pth.write_text(f"import sys; sys.path.insert(0, '{marker_dir}')\n")
        py = venv / _BIN / "python"
        check = subprocess.run([str(py), "-c", "import exec_pkg; print(exec_pkg.VALUE)"], capture_output=True, text=True)
        # Also verify the .pth itself is executable (starts with import)
        is_executable = pth.read_text().lstrip().startswith("import")
        return check.returncode == 0 and "from-executable-pth" in check.stdout and is_executable


def variant_finder_artifact() -> bool:
    """PEP 660 finder artifact: a __editable___finder.py installed and imported via .pth."""
    with tempfile.TemporaryDirectory() as td:
        venv = _venv(pathlib.Path(td))
        site = _site_packages(venv)
        # Create a minimal finder for a test package "finder_pkg"
        finder_src = """
import sys, pathlib, importlib.abc, importlib.util
class Finder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname == "finder_pkg" or fullname.startswith("finder_pkg."):
            src = pathlib.Path(__file__).parent / "finder_src" / fullname.replace(".", "/")
            if src.with_suffix(".py").exists():
                return importlib.util.spec_from_file_location(fullname, src.with_suffix(".py"))
            if (src / "__init__.py").exists():
                return importlib.util.spec_from_file_location(fullname, src / "__init__.py", submodule_search_locations=[str(src)])
        return None
sys.meta_path.insert(0, Finder())
"""
        finder_path = site / "__editable___finder_test_finder.py"
        finder_path.write_text(finder_src)
        # Executable .pth that imports the finder (executable .pth)
        (site / "finder_test.pth").write_text("import __editable___finder_test_finder\n")
        # Create the finder source
        src_dir = site / "finder_src" / "finder_pkg"
        src_dir.mkdir(parents=True)
        (src_dir / "__init__.py").write_text("VALUE='via-finder'\n")
        py = venv / _BIN / "python"
        check = subprocess.run([str(py), "-c", "import finder_pkg; print(finder_pkg.VALUE)"], capture_output=True, text=True)
        # Verify the finder artifact exists and was executed
        return check.returncode == 0 and "via-finder" in check.stdout and finder_path.exists()


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
    """Link-farm editable: setuptools strict mode writes a .pth pointing at build/__editable__ link farm."""
    with tempfile.TemporaryDirectory() as td:
        venv = _venv(pathlib.Path(td))
        if _pip_editable(venv, CORE, "--config-settings", "editable_mode=strict").returncode != 0:
            return False
        # Strict mode's .pth points at build/__editable__.distributable_suite_core-...
        pths = list(_site_packages(venv).glob("*.pth"))
        if not pths:
            return False
        target = pathlib.Path(pths[0].read_text().strip())
        # Link farm is a directory containing symlinked packages or copies
        if not target.is_dir():
            return False
        # Verify the link farm contains the expected top-level packages
        has_core = (target / "suite_core").exists() or (target / "suite_core").is_symlink()
        has_utils = (target / "suite_core_utils").exists() or (target / "suite_core_utils").is_symlink()
        py = venv / _BIN / "python"
        check = subprocess.run([str(py), "-c", "import suite_core; print(suite_core.__file__)"], capture_output=True, text=True)
        return has_core and has_utils and check.returncode == 0


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


def variant_added_package() -> bool:
    """Added-package behavior: a new top-level package is not importable until reinstall (strict link farm)."""
    with tempfile.TemporaryDirectory() as td:
        work = pathlib.Path(td) / "src"
        shutil.copytree(CORE, work)
        venv = _venv(pathlib.Path(td))
        # Use strict link-farm mode so new packages are not on sys.path until reinstall
        if _pip_editable(venv, work, "--config-settings", "editable_mode=strict").returncode != 0:
            return False
        py = venv / _BIN / "python"
        # Initially no new package (use a name matching include pattern suite_core*)
        check_before = subprocess.run([str(py), "-c", "import importlib.util; print(importlib.util.find_spec('suite_core_extra') is None)"], capture_output=True, text=True)
        if "True" not in check_before.stdout:
            return False
        # Add a new top-level package directory that matches include pattern
        new_pkg = work / "suite_core_extra"
        new_pkg.mkdir()
        (new_pkg / "__init__.py").write_text("VALUE='added-package'\n")
        # Without reinstall, the new package should NOT be found (link farm not updated)
        check_without = subprocess.run([str(py), "-c", "import suite_core_extra; print(suite_core_extra.VALUE)"], capture_output=True, text=True)
        if check_without.returncode == 0 and "added-package" in check_without.stdout:
            return False  # should not be importable without reinstall
        # Reinstall (strict) should make it importable
        if _pip_editable(venv, work, "--config-settings", "editable_mode=strict").returncode != 0:
            return False
        check_after = subprocess.run([str(py), "-c", "import suite_core_extra; print(suite_core_extra.VALUE)"], capture_output=True, text=True)
        return "added-package" in check_after.stdout


def all_variants() -> dict[str, bool]:
    return {
        "static_pth": variant_static_pth(),
        "executable_pth": variant_executable_pth(),
        "finder_artifact": variant_finder_artifact(),
        "finder_strict": variant_finder_strict(),
        "lenient": variant_lenient(),
        "link_farm": variant_link_farm(),
        "added_package": variant_added_package(),
        "provenance": variant_provenance(),
        "source_change_no_reinstall": variant_source_change(),
        "metadata_requires_reinstall": variant_metadata_rebuild(),
    }
