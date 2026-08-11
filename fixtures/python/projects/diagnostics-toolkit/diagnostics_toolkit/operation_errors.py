"""Missing/invalid operation exception taxonomy (PY-CAN-DIAG-003).

Triggers NameError, UnboundLocalError, AttributeError, KeyError,
IndexError, and TypeError as distinct runtime operation errors.
"""

from __future__ import annotations


def trigger_name_error() -> dict[str, object]:
    """Reference an undefined name → NameError."""

    try:
        _ = undefined_name_xyz  # type: ignore[name-defined]
        return {"raised": False}
    except NameError as exc:
        return {"raised": True, "kind": "NameError", "msg": str(exc)}


def trigger_unbound_local() -> dict[str, object]:
    """Read a local before its binding → UnboundLocalError."""

    def inner() -> str:
        try:
            # mypy would classify as local due to later assignment.
            print(unbound_local_var)  # type: ignore[name-defined]
            unbound_local_var = "assigned"  # noqa: F841
            return "no-error"
        except UnboundLocalError as exc:
            return f"unbound:{exc}"
        except NameError as exc:  # fallback on some runtimes
            return f"name:{exc}"

    result = inner()
    return {"raised": "unbound" in result or "name" in result, "detail": result}


def trigger_attribute_error() -> dict[str, object]:
    """Access a missing attribute → AttributeError."""

    class Holder:
        existing = 1

    try:
        _ = Holder().missing_attribute_xyz  # type: ignore[attr-defined]
        return {"raised": False}
    except AttributeError as exc:
        return {"raised": True, "kind": "AttributeError", "msg": str(exc)}


def trigger_key_error() -> dict[str, object]:
    """Lookup a missing mapping key → KeyError."""

    mapping = {"alpha": 1}
    try:
        _ = mapping["missing_key_xyz"]
        return {"raised": False}
    except KeyError as exc:
        return {"raised": True, "kind": "KeyError", "key": exc.args[0] if exc.args else None}


def trigger_index_error() -> dict[str, object]:
    """Index beyond sequence bounds → IndexError."""

    seq = [1, 2, 3]
    try:
        _ = seq[99]
        return {"raised": False}
    except IndexError as exc:
        return {"raised": True, "kind": "IndexError", "msg": str(exc)}


def trigger_type_error() -> dict[str, object]:
    """Apply an operation to an incompatible type → TypeError."""

    try:
        _ = len(123)  # type: ignore[arg-type]
        return {"raised": False}
    except TypeError as exc:
        return {"raised": True, "kind": "TypeError", "msg": str(exc)}


def trigger_type_error_via_operator() -> dict[str, object]:
    """Type mismatch via unsupported operand types."""

    try:
        _ = "text" + 123  # type: ignore[operator]
        return {"raised": False}
    except TypeError as exc:
        return {"raised": True, "kind": "TypeError", "msg": str(exc)}


def all_operation_error_demos() -> dict[str, object]:
    """Run every operation-error variant."""

    return {
        "name": trigger_name_error(),
        "unbound_local": trigger_unbound_local(),
        "attribute": trigger_attribute_error(),
        "key": trigger_key_error(),
        "index": trigger_index_error(),
        "type_len": trigger_type_error(),
        "type_operator": trigger_type_error_via_operator(),
    }
