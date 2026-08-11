"""``runpy`` entry demonstrations (PY-CAN-MOD-001).

Exercises ``runpy.run_module`` and ``runpy.run_path`` against the same
declaration-bearing source used for import / script / ``-m`` forms.
All variants run in the child-process context when invoked via subprocess.
"""

from __future__ import annotations

import pathlib
import runpy
import sys


def run_via_run_module(mod_name: str = "content_library.entry_declarations") -> dict[str, object]:
    """Execute a module as ``__main__`` via :func:`runpy.run_module`."""
    # ``run_name`` defaults to ``__main__`` inside runpy; alter to preserve caller.
    result = runpy.run_module(mod_name, run_name="__runpy_demo__")
    return {k: result[k] for k in ("__name__", "MODULE_LABEL") if k in result}


def run_via_run_path(path: pathlib.Path | None = None) -> dict[str, object]:
    """Execute the declaration source as a file via :func:`runpy.run_path`."""
    target = path or pathlib.Path(__file__).with_name("entry_declarations.py")
    result = runpy.run_path(str(target), run_name="__run_path_demo__")
    return {k: result[k] for k in ("__name__", "MODULE_LABEL") if k in result}


def launcher_child_process_examples() -> list[list[str]]:
    """Return command lines that exercise launcher / child-process entry forms.

    Callers spawn these via ``subprocess`` with ``sys.executable`` in the
    child-process / interpreter-flags context.
    """
    base = pathlib.Path(__file__).parent
    entry_file = base / "entry_declarations.py"
    return [
        [sys.executable, str(entry_file)],
        [sys.executable, "-m", "content_library.entry_declarations"],
        [sys.executable, "-m", "content_library"],
        [sys.executable, "-c", "import runpy; runpy.run_module('content_library.entry_declarations', run_name='__main__')"],
    ]
