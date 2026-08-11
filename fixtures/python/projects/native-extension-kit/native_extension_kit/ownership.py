"""PY-CAN-NATIVE-003: native ownership and exception translation."""

from __future__ import annotations

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
    result["pairing"] = "Correct pairing: PyErr_SetString + return NULL; automated binding (pybind11) contrast: raises via C++ exception translator"
    result["immortal_note"] = "Immortal objects (PEP 683) are not a contract for ownership demo"
    return result


def leak_overdecrement_notes() -> dict[str, str]:
    return {
        "leak": "Forgetting Py_DECREF on owned reference leaks",
        "over_decrement": "Extra Py_DECREF causes use-after-free / crash",
        "system_error": "Returning NULL without error or non-NULL with error triggers SystemError",
    }


__all__ = [
    "owned_reference_demo",
    "borrowed_reference_demo",
    "container_transfer_demo",
    "error_translation_demo",
    "leak_overdecrement_notes",
]
