"""PKG-018 build hooks and config settings, observed by driving setuptools.build_meta.

The hooks are invoked directly through ``setuptools.build_meta`` inside an
isolated venv that has only the vendored ``setuptools==84.0.0`` installed, from a
throwaway copy of the distribution (so tracked source is never mutated). Every
claimed hook runs, the prepared and final wheel metadata are compared, and a
namespaced config setting is shown to be consumed by observing the build tag it
produces in the wheel filename.
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

HOOK_SEQUENCE = [
    "get_requires_for_build_wheel",
    "prepare_metadata_for_build_wheel",
    "build_wheel",
    "get_requires_for_build_sdist",
    "build_sdist",
    "get_requires_for_build_editable",
    "prepare_metadata_for_build_editable",
    "build_editable",
]

# A build number passed as a bdist_wheel build-option; setuptools encodes it as
# the wheel's build tag (the "-7-" segment of the filename), so seeing it proves
# the config setting reached the backend.
CONFIG_SETTING = {"--build-option": ["--build-number", "7"]}

EMPTY_REQUIRES_CLAIM = "setuptools.build_meta 84.0.0 get_requires_for_build_* returns [] with no setup_requires (lines 265-310, 435-438)"

_DRIVER = r'''
import json, os, sys, tempfile, zipfile
import setuptools.build_meta as bm

os.chdir(sys.argv[1])
out = {}
out["get_requires_for_build_wheel"] = bm.get_requires_for_build_wheel({})
out["get_requires_for_build_sdist"] = bm.get_requires_for_build_sdist({})
out["get_requires_for_build_editable"] = bm.get_requires_for_build_editable({})

md = tempfile.mkdtemp()
dist_info = bm.prepare_metadata_for_build_wheel(md, {})
prepared = open(os.path.join(md, dist_info, "METADATA")).read()

wd = tempfile.mkdtemp()
wheel = bm.build_wheel(wd, {"--build-option": ["--build-number", "7"]})
out["build_wheel"] = wheel
with zipfile.ZipFile(os.path.join(wd, wheel)) as zf:
    final = [zf.read(n).decode() for n in zf.namelist() if n.endswith(".dist-info/METADATA")][0]
out["prepared_matches_final_metadata"] = (prepared == final)
out["config_setting_consumed"] = "-7-" in wheel

ed = tempfile.mkdtemp()
out["prepare_metadata_for_build_editable"] = bm.prepare_metadata_for_build_editable(ed, {})
ewd = tempfile.mkdtemp()
out["build_editable"] = bm.build_editable(ewd, {})

sd = tempfile.mkdtemp()
out["build_sdist"] = bm.build_sdist(sd, {})
print(json.dumps(out))
'''


def observe_hooks_offline() -> dict:
    """Drive every build hook offline and return the observed results."""
    import json
    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        venv = tmp / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
        pip = venv / _BIN / "pip"
        py = venv / _BIN / "python"
        setup = subprocess.run(
            [str(pip), "install", "--no-index", "--find-links", str(WHEELHOUSE), "setuptools==84.0.0"],
            capture_output=True, text=True,
        )
        if setup.returncode != 0:
            return {"setuptools_installed": False}

        # Copy the distribution so build_meta's egg-info/build artifacts never
        # land in tracked source.
        work = tmp / "src"
        shutil.copytree(CORE, work)
        driver = tmp / "driver.py"
        driver.write_text(_DRIVER)
        run = subprocess.run([str(py), str(driver), str(work)], capture_output=True, text=True)
        if run.returncode != 0:
            return {"driver_ok": False, "stderr": run.stderr[-500:]}
        observed = json.loads(run.stdout.strip().splitlines()[-1])

    return {
        "get_requires_for_build_wheel_empty": observed["get_requires_for_build_wheel"] == [],
        "get_requires_for_build_sdist_empty": observed["get_requires_for_build_sdist"] == [],
        "get_requires_for_build_editable_empty": observed["get_requires_for_build_editable"] == [],
        "prepared_matches_final_metadata": observed["prepared_matches_final_metadata"],
        "config_setting_consumed": observed["config_setting_consumed"],
        "editable_metadata_prepared": bool(observed["prepare_metadata_for_build_editable"]),
        "editable_wheel_built": ".editable-" in observed["build_editable"] or observed["build_editable"].endswith(".whl"),
        "sdist_built": observed["build_sdist"].endswith(".tar.gz"),
    }


def config_settings_demo() -> dict:
    return {
        "setting": CONFIG_SETTING,
        "observable_as": "wheel build tag (the -7- segment of the wheel filename)",
        "backend_spelling": "tool.setuptools table versus --config-settings namespace",
    }
