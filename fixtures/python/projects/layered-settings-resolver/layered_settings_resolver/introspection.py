"""Namespace, frame, and code introspection (PY-CAN-BIND-009)."""

from __future__ import annotations

import sys
from types import FrameType


def globals_locals_vars() -> dict[str, object]:
    """Inspect module globals, locals, and `vars()` snapshots."""

    module_globals = globals()
    module_locals = locals()
    module_vars = vars()
    return {
        "globals_keys": sorted(module_globals.keys())[:5],
        "locals_keys": sorted(module_locals.keys())[:5],
        "vars_keys": sorted(module_vars.keys())[:5],
    }


def code_object_names(function: callable) -> dict[str, tuple[str, ...]]:
    """Read code-object name tuples without asserting private layout."""

    code = function.__code__
    return {
        "co_varnames": code.co_varnames,
        "co_names": code.co_names,
        "co_freevars": code.co_freevars,
    }


def closure_cells(function: callable) -> list[str]:
    """List closure cell contents for a nested callable."""

    if function.__closure__ is None:
        return []
    return [cell.cell_contents for cell in function.__closure__]


def frame_locals_snapshot() -> FrameType | None:
    """Capture the current frame without retaining it beyond the call."""

    frame = sys._getframe()
    _ = frame.f_locals
    return frame


def optimized_locals_reader(items: list[int]) -> int:
    """Exercise optimized locals in a tight loop."""

    total = 0
    for item in items:
        total += item
    return total
