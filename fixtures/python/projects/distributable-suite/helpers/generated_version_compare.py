"""PY-CAN-INT-005 generated version read across source tree, sdist, wheel, installs."""

from __future__ import annotations

import ast
import pathlib
import tarfile
import zipfile

GENERATED_SUFFIX = "suite_core/_generated_version.py"


def parse_version(source: str) -> str:
    """Extract ``__version__`` from generated-module source text."""
    module = ast.parse(source)
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__version__":
                    return ast.literal_eval(node.value)
    return ""


def read_source_tree_version(generated_file: pathlib.Path) -> str:
    return parse_version(generated_file.read_text())


def read_sdist_version(sdist: pathlib.Path) -> str:
    with tarfile.open(sdist) as tf:
        member = next((m for m in tf.getmembers() if m.name.endswith(GENERATED_SUFFIX)), None)
        if member is None:
            return ""
        extracted = tf.extractfile(member)
        return parse_version(extracted.read().decode()) if extracted else ""


def read_wheel_version(wheel: pathlib.Path) -> str:
    with zipfile.ZipFile(wheel) as zf:
        for name in zf.namelist():
            if name.endswith(GENERATED_SUFFIX):
                return parse_version(zf.read(name).decode())
    return ""


def editable_bypass_note() -> str:
    return "an editable install reads the source tree directly; a stale generated file would show a mismatch"


def missing_vcs_data_note() -> str:
    return "with no version-control data the generator would fall back to version 0.0.0"
