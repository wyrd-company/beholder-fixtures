"""PY-CAN-NATIVE-003: native ownership and exception translation."""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

try:
    from . import _native_single  # type: ignore[import-not-found]
except ImportError:
    _native_single = None  # type: ignore[assignment]


def owned_reference_demo() -> dict[str, object]:
    if _native_single is None:
        return {"available": False}
    s = _native_single.owned_new_string("owned")
    return {"value": s, "owned": True, "note": "PyUnicode_FromString returns owned reference"}


def borrowed_reference_demo() -> dict[str, object]:
    if _native_single is None:
        return {"available": False}
    lst = ["alpha", "beta", "gamma"]
    item = _native_single.borrowed_peek(lst, 1)
    return {
        "item": item,
        "borrowed_source": "PyList_GetItem returns borrowed; callee INCREFs before return",
        "list": lst,
    }


def container_transfer_demo() -> dict[str, object]:
    if _native_single is None:
        return {"available": False}
    lst: list[object] = []
    _native_single.container_transfer(lst, "transferred")
    tup = _native_single.tuple_steal_demo("a", "b")
    return {
        "list_after_append": lst,
        "tuple": tup,
        "note_append": "PyList_Append increments; caller retains ownership",
        "note_tuple": "PyTuple_SetItem steals reference",
    }


def error_translation_demo() -> dict[str, object]:
    if _native_single is None:
        return {"available": False}
    result: dict[str, object] = {}
    try:
        _native_single.raise_native_error("native failure")
    except ValueError as exc:
        result["caught_value_error"] = str(exc)
    try:
        _native_single.raise_without_error()
    except SystemError as exc:
        result["system_error_no_error"] = str(exc)
    try:
        _native_single.return_with_error_set()
    except SystemError as exc:
        result["system_error_with_error"] = str(exc)
    result["pairing"] = "Correct pairing: PyErr_SetString + return NULL"
    result["immortal_note"] = "Immortal objects (PEP 683) are not a contract for ownership demo"
    return result


def leak_demo() -> dict[str, object]:
    """Exercise the real leak structure: _native_single.c:leak_reference takes a
    strong reference and never releases it, so the object's refcount rises by one
    and stays there."""
    if _native_single is None:
        return {"available": False}
    obj = object()
    before = sys.getrefcount(obj)
    _native_single.leak_reference(obj)
    after = sys.getrefcount(obj)
    return {
        "available": True,
        "before": before,
        "after": after,
        "leaked": after - before,
        "source": "_native_single.c:leak_reference — Py_INCREF with no matching Py_DECREF",
    }


def over_decrement_demo_isolated() -> dict[str, object]:
    """Exercise the real over-decrement structure in an isolated subprocess.
    _native_single.c:over_decrement releases a reference it never owned; unpaired
    this underflows the refcount and can free a live object, so the call is run in
    a child process. The child inflates the target refcount first so the observed
    effect is a deterministic single decrement, then restores balance before
    exit."""
    project_root = str(Path(__file__).resolve().parent.parent)
    code = textwrap.dedent("""\
        import ctypes, sys
        from native_extension_kit import _native_single
        obj = object()
        # Inflate so a single unowned decrement neither underflows nor frees obj.
        ctypes.pythonapi.Py_IncRef(ctypes.py_object(obj))
        ctypes.pythonapi.Py_IncRef(ctypes.py_object(obj))
        before = sys.getrefcount(obj)
        _native_single.over_decrement(obj)   # real unbalanced Py_DECREF in C
        after = sys.getrefcount(obj)
        # Restore the reference the over-decrement removed so shutdown is clean.
        ctypes.pythonapi.Py_IncRef(ctypes.py_object(obj))
        print(f"over_decrement {before} -> {after}")
    """)
    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        timeout=5,
        cwd=project_root,
    )
    return {
        "isolated": True,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "returncode": proc.returncode,
        "note": "Unpaired Py_DECREF underflows refcount and can crash; isolated via subprocess",
        "source": "_native_single.c:over_decrement — Py_DECREF of an unowned reference",
    }


def automated_binding_contrast_demo() -> dict[str, object]:
    """Contrast manual per-site error setting with an automated translator.
    _native_single.c:raise_native_error is the manual form (a hand-written
    PyErr_SetString at the call site); _native_single.c:automated_translate is a
    single table-driven dispatcher that any call site shares, modeling the
    translation layer a binding generator emits. Both are native C structures."""
    if _native_single is None:
        return {"available": False}
    manual: dict[str, object] = {}
    try:
        _native_single.raise_native_error("manual c-api failure")
    except ValueError as exc:
        manual["manual_c_api"] = f"PyErr_SetString + NULL -> ValueError: {exc}"

    automated: dict[str, object] = {}
    try:
        _native_single.automated_binding_raise(3)  # KIT_VALUE -> ValueError
    except ValueError as exc:
        automated["automated_value"] = f"automated_translate(KIT_VALUE) -> ValueError: {exc}"
    try:
        _native_single.automated_binding_raise(1)  # KIT_RANGE -> IndexError
    except IndexError as exc:
        automated["automated_range"] = f"automated_translate(KIT_RANGE) -> IndexError: {exc}"
    return {
        "available": True,
        "manual": manual,
        "automated": automated,
        "contrast": "manual per-site PyErr_SetString vs single table-driven automated translator",
    }


__all__ = [
    "owned_reference_demo",
    "borrowed_reference_demo",
    "container_transfer_demo",
    "error_translation_demo",
    "leak_demo",
    "over_decrement_demo_isolated",
    "automated_binding_contrast_demo",
]
