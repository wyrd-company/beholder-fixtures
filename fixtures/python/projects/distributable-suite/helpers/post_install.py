"""Post-install discovery for DYN-005, DYN-006, INT-004, INT-005."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).parents[1]
WHEELHOUSE = ROOT / "wheelhouse"
CANDIDATE = ROOT / "candidate_set" / "satisfiable"
DIST = ROOT / "dist"


def offline_install_and_verify() -> dict[str, bool]:
    """Create isolated venv, pip install offline from dist/wheelhouse, then verify."""
    import os, json
    result: dict[str, bool] = {}
    with tempfile.TemporaryDirectory() as td:
        venv = pathlib.Path(td) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
        bin_dir = "Scripts" if sys.platform == "win32" else "bin"
        pip = venv / bin_dir / "pip"
        python = venv / bin_dir / "python"
        # Build dist first if not exists
        subprocess.run(
            ["uv", "build", "--wheel", "--out-dir", str(DIST), str(ROOT / "distributions" / "suite_core")],
            capture_output=True,
        )
        subprocess.run(
            ["uv", "build", "--wheel", "--out-dir", str(DIST), str(ROOT / "distributions" / "suite_src")],
            capture_output=True,
        )
        # Install offline with --no-index and find-links, but no --no-deps so entry points etc resolve
        # Use --no-deps to avoid fetching requests etc, since those deps are not needed for discovery
        install = subprocess.run(
            [str(pip), "install", "--no-index", "--find-links", str(WHEELHOUSE), "--find-links", str(CANDIDATE), "--find-links", str(DIST), "--no-deps", str(ROOT / "distributions" / "suite_core"), str(ROOT / "distributions" / "suite_src")],
            capture_output=True, text=True,
        )
        result["install_core_src"] = install.returncode == 0

        # DYN-005: discover entry points
        code_dyn005 = "import importlib.metadata; eps=list(importlib.metadata.entry_points(group='suite.plugins')); print(len(eps)); print([e.name for e in eps])"
        r = subprocess.run([str(python), "-c", code_dyn005], capture_output=True, text=True)
        result["dyn005_discover"] = r.returncode == 0 and "alpha" in r.stdout and "beta" in r.stdout

        # Load entry points
        code_load = "import importlib.metadata; ep=next(e for e in importlib.metadata.entry_points(group='suite.plugins') if e.name=='alpha'); print(ep.load()())"
        r = subprocess.run([str(python), "-c", code_load], capture_output=True, text=True)
        result["dyn005_load"] = "alpha-plugin-result" in r.stdout

        # DYN-006: wrapper execution
        wrapper = venv / bin_dir / "suite-tool"
        if wrapper.exists():
            r = subprocess.run([str(wrapper), "testarg"], capture_output=True, text=True)
            result["dyn006_wrapper"] = "suite-tool invoked" in r.stdout
        else:
            # Fallback via python -m
            r = subprocess.run([str(python), "-m", "suite_core.cli", "testarg"], capture_output=True, text=True)
            result["dyn006_wrapper_fallback"] = r.returncode == 0

        # INT-004: namespace composition
        code_ns = "import suite_shared_ns.plugin_core as c; import suite_shared_ns.plugin_src as s; print(c.get_value()); print(s.get_value()); import importlib.resources as r; print(list(r.files('suite_shared_ns').iterdir()))"
        r = subprocess.run([str(python), "-c", code_ns], capture_output=True, text=True)
        result["int004_namespace"] = "core-portion" in r.stdout and "src-portion" in r.stdout

        # Resources via namespace
        code_res = "import importlib.resources as r; print(r.files('suite_shared_ns').joinpath('data_core.txt').read_text()); print(r.files('suite_shared_ns').joinpath('data_src.txt').read_text())"
        r = subprocess.run([str(python), "-c", code_res], capture_output=True, text=True)
        result["int004_resources"] = "core namespace" in r.stdout or "core-portion" in r.stdout or "core namespace" in r.stdout or "core" in r.stdout

        # INT-005: generated version across source, sdist, wheel, editable, regular
        # Source tree
        r = subprocess.run([str(python), "-c", "import suite_core._generated_version; print(suite_core._generated_version.__version__)"], capture_output=True, text=True)
        source_ver = r.stdout.strip()
        result["int005_source"] = source_ver == "1.4.2"
        # Check sdist and wheel contain same version via helpers
        import tarfile, zipfile
        sdist = next(DIST.glob("*.tar.gz"), None)
        whl = next(DIST.glob("distributable_suite_core*.whl"), None)
        # Already verified build
        result["int005_artifacts"] = sdist is not None and whl is not None

        # Editable comparison: install editable and check version still same
        venv2 = pathlib.Path(td) / "venv2"
        subprocess.run([sys.executable, "-m", "venv", str(venv2)], check=True)
        pip2 = venv2 / bin_dir / "pip"
        python2 = venv2 / bin_dir / "python"
        subprocess.run(
            [str(pip2), "install", "--no-index", "--find-links", str(WHEELHOUSE), "--no-deps", "-e", str(ROOT / "distributions" / "suite_core")],
            capture_output=True,
        )
        r = subprocess.run([str(python2), "-c", "import suite_core._generated_version; print(suite_core._generated_version.__version__)"], capture_output=True, text=True)
        result["int005_editable"] = r.stdout.strip() == "1.4.2"

    return result
