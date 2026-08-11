"""PY-CAN-INT-005 generated version across source tree, sdist, wheel, editable."""

from __future__ import annotations

import pathlib
import tarfile
import zipfile

GENERATED_PATH = pathlib.Path("suite_core/_generated_version.py")
SOURCE_VERSION_ATTR = "suite_core._generated_version.__version__"


def read_source_tree_version() -> str:
    import suite_core._generated_version as gv

    return gv.__version__


def read_sdist_version(sdist: pathlib.Path) -> str:
    with tarfile.open(sdist) as tf:
        member = [m for m in tf.getmembers() if m.name.endswith("suite_core/_generated_version.py")]
        if not member:
            return ""
        f = tf.extractfile(member[0])
        assert f is not None
        return f.read().decode()


def read_wheel_version(wheel: pathlib.Path) -> str:
    with zipfile.ZipFile(wheel) as zf:
        for name in zf.namelist():
            if name.endswith("suite_core/_generated_version.py"):
                return zf.read(name).decode()
    return ""


def editable_bypass_note() -> str:
    return "editable install bypasses wheel copy and reads source tree directly; stale generated file would show mismatch"


def missing_vcs_data_note() -> str:
    return "missing version-control data (e.g. git not available) yields fallback version 0.0.0"
