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


def frame_locals_snapshot() -> dict[str, object]:
    """Exercise `locals()` snapshots versus `frame.f_locals` write-through."""

    fast_counter = 0
    locals_snapshot = dict(locals())
    frame = sys._getframe()
    frame_locals = frame.f_locals
    frame_locals["fast_counter"] = 7
    return {
        "snapshot_before": locals_snapshot.get("fast_counter"),
        "live_after_frame_write": fast_counter,
        "frame_locals_after": frame_locals.get("fast_counter"),
    }


def optimized_locals_reader(items: list[int]) -> dict[str, object]:
    """Exercise optimized locals in a loop and snapshot them with `locals()`."""

    total = 0
    snapshots: list[dict[str, object]] = []
    for item in items:
        total += item
        snapshots.append(dict(locals()))
    return {"total": total, "snapshots": snapshots}
