"""Post-install discovery for DYN-005, DYN-006, INT-004, INT-005, executed offline.

Installs the core and src distributions offline from the vendored wheelhouse into
throwaway venvs and verifies entry-point discovery, the generated console-script
wrapper, namespace composition with resources, and the generated version read and
compared across all five forms: source tree, source distribution, wheel, regular
install, and editable install.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile

import generated_version_compare as gvc

ROOT = pathlib.Path(__file__).parents[1]
WHEELHOUSE = ROOT / "wheelhouse"
CORE = ROOT / "distributions" / "suite_core"
SRC = ROOT / "distributions" / "suite_src"
GENERATED_FILE = CORE / "suite_core" / "_generated_version.py"
_BIN = "Scripts" if sys.platform == "win32" else "bin"
_OFFLINE_INDEX = ["--offline", "--no-index", "--find-links", str(WHEELHOUSE)]


def _build(kind: str, project: pathlib.Path, out_dir: pathlib.Path) -> pathlib.Path | None:
    result = subprocess.run(
        ["uv", "build", kind, *_OFFLINE_INDEX, "--out-dir", str(out_dir), str(project)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    pattern = "*.tar.gz" if kind == "--sdist" else "distributable_suite_core-*.whl"
    matches = sorted(out_dir.glob(pattern))
    return matches[-1] if matches else None


def offline_install_and_verify() -> dict[str, object]:
    result: dict[str, object] = {}
    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        dist = tmp / "dist"
        dist.mkdir()

        core_sdist = _build("--sdist", CORE, dist)
        core_wheel = _build("--wheel", CORE, dist)
        # src wheel is needed for namespace / entry-point discovery.
        subprocess.run(["uv", "build", "--wheel", *_OFFLINE_INDEX, "--out-dir", str(dist), str(SRC)], capture_output=True)
        result["core_sdist_built"] = core_sdist is not None
        result["core_wheel_built"] = core_wheel is not None
        if core_sdist is None or core_wheel is None:
            return result

        # Regular install of core + src into venv1.
        venv1 = tmp / "venv1"
        subprocess.run([sys.executable, "-m", "venv", str(venv1)], check=True)
        pip1 = venv1 / _BIN / "pip"
        py1 = venv1 / _BIN / "python"
        install = subprocess.run(
            [str(pip1), "install", "--no-index", "--find-links", str(WHEELHOUSE), "--find-links", str(dist),
             "--no-deps", "distributable-suite-core", "distributable-suite-src"],
            capture_output=True, text=True,
        )
        result["install_core_src"] = install.returncode == 0

        # DYN-005: entry-point discovery and load.
        discover = subprocess.run(
            [str(py1), "-c", "import importlib.metadata as m; eps=list(m.entry_points(group='suite.plugins')); print(sorted(e.name for e in eps))"],
            capture_output=True, text=True, cwd=td,
        )
        result["dyn005_discover"] = "alpha" in discover.stdout and "beta" in discover.stdout
        load = subprocess.run(
            [str(py1), "-c", "import importlib.metadata as m; ep=next(e for e in m.entry_points(group='suite.plugins') if e.name=='alpha'); print(ep.load()())"],
            capture_output=True, text=True, cwd=td,
        )
        result["dyn005_load"] = "alpha-plugin-result" in load.stdout

        # DYN-006: console-script wrapper executes.
        wrapper = venv1 / _BIN / "suite-tool"
        if wrapper.exists():
            wr = subprocess.run([str(wrapper), "testarg"], capture_output=True, text=True)
            result["dyn006_wrapper"] = "suite-tool invoked" in wr.stdout
        else:
            result["dyn006_wrapper"] = False

        # INT-004: namespace composition and resources.
        ns = subprocess.run(
            [str(py1), "-c", "import suite_shared_ns.plugin_core as c; import suite_shared_ns.plugin_src as s; print(c.get_value(), s.get_value())"],
            capture_output=True, text=True, cwd=td,
        )
        result["int004_namespace"] = "core-portion" in ns.stdout and "src-portion" in ns.stdout
        res = subprocess.run(
            [str(py1), "-c", "import importlib.resources as r; print(r.files('suite_shared_ns').joinpath('data_core.txt').read_text()); print(r.files('suite_shared_ns').joinpath('data_src.txt').read_text())"],
            capture_output=True, text=True, cwd=td,
        )
        result["int004_resources"] = res.returncode == 0 and len(res.stdout.strip().splitlines()) >= 2

        # INT-005: read the generated version across all five forms.
        regular = subprocess.run(
            [str(py1), "-c", "import suite_core._generated_version as g; print(g.__version__)"],
            capture_output=True, text=True, cwd=td,
        )
        venv2 = tmp / "venv2"
        subprocess.run([sys.executable, "-m", "venv", str(venv2)], check=True)
        pip2 = venv2 / _BIN / "pip"
        py2 = venv2 / _BIN / "python"
        subprocess.run(
            [str(pip2), "install", "--no-index", "--find-links", str(WHEELHOUSE), "--no-deps", "-e", str(CORE)],
            capture_output=True,
        )
        editable = subprocess.run(
            [str(py2), "-c", "import suite_core._generated_version as g; print(g.__version__)"],
            capture_output=True, text=True, cwd=td,
        )
        versions = {
            "source_tree": gvc.read_source_tree_version(GENERATED_FILE),
            "sdist": gvc.read_sdist_version(core_sdist),
            "wheel": gvc.read_wheel_version(core_wheel),
            "regular_install": regular.stdout.strip(),
            "editable_install": editable.stdout.strip(),
        }
        result["int005_versions"] = versions
        result["int005_all_equal"] = len(set(versions.values())) == 1 and versions["source_tree"] == "1.4.2"

    return result
