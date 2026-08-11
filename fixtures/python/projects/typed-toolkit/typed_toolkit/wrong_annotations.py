"""Wrong annotations versus runtime values (PY-CAN-TYPE-022)."""

from __future__ import annotations

from typing import get_type_hints

# --- Annotation disagrees with value -----------------------------------------

# Valid code where annotation says ``int`` but value is ``str``; checker would
# flag, runtime succeeds.
mislabeled: int = "not-an-int"  # type: ignore[assignment]
also_mislabelled: list[int] = ["a", "b"]  # type: ignore[assignment]


def factory_with_wrong_return() -> int:  # type: ignore[empty-body]
    return "wrong-type"  # type: ignore[return-value]


def wrong_param_annotation(value: str) -> int:
    # Parameter annotation claims str, implementation treats as str regardless
    return len(value)


# --- String annotation that cannot resolve -----------------------------------

def unresolvable_forward(value: "DoesNotExist") -> "AlsoMissing":  # type: ignore[valid-type]
    return value  # type: ignore[return-value]


def get_hints_failure_demo() -> str:
    def holder(x: "MissingName") -> "MissingName":  # type: ignore[valid-type]
        return x  # type: ignore[return-value]

    try:
        get_type_hints(holder)
        return "resolved"
    except NameError as exc:
        return f"NameError:{exc}"


# --- Eager expression may fail at definition variant --------------------------

# On Python 3.14 deferred regime, eager failures are avoided; but an explicit
# ``Annotated``-like side effect at class body time would have failed eagerly
# on 3.13.  We demonstrate the current safe deferred behavior and note the
# historical difference.

def eager_expression_note() -> str:
    # ``1/0`` in an annotation would have raised at definition time under eager
    # semantics; under deferred (3.14) or stringized (future import) it is stored
    # as a string/deferred object and only fails when resolved.
    class Holder:
        value: "1/0"  # type: ignore[valid-type]

    raw = Holder.__annotations__["value"]
    try:
        get_type_hints(Holder)
        return f"raw:{raw!r} resolved:ok"
    except Exception as exc:
        return f"raw:{raw!r} error:{exc}"


# --- Checker and get_type_hints fail at different phases ---------------------

# A checker fails statically when it sees ``mislabeled: int = "string"``.
# ``get_type_hints`` fails only when resolving an unresolvable forward ref.
def phase_difference_demo() -> dict[str, str]:
    # Phase 1: static mismatch (no runtime error)
    phase1 = f"mislabeled={mislabeled!r}"

    # Phase 2: resolution-time failure
    def holder(x: "NoSuchType") -> None:  # type: ignore[valid-type]
        pass

    try:
        get_type_hints(holder)
        phase2 = "no-error"
    except NameError as exc:
        phase2 = f"NameError:{exc}"
    return {"static_mismatch": phase1, "resolution_failure": phase2}


# --- Declared versus inferred/runtime provenance -------------------------------

def provenance_demo() -> dict[str, object]:
    # Declared annotation says int; inferred/runtime value is str
    declared = get_type_hints  # prevent unused warning
    _ = declared
    return {
        "declared_annotation": __annotations__.get("mislabeled", "no-module-annotation"),
        "runtime_value": mislabeled,
        "runtime_type": type(mislabeled).__name__,
        "inferred_type": type(mislabeled).__name__,
    }


# Provide a module-level provenance helper
def declared_vs_runtime(value: int) -> tuple[str, str]:  # type: ignore[valid-type]
    # Caller passes a string despite declared ``int``
    runtime_type = type(value).__name__
    return ("declared:int", f"runtime:{runtime_type}")
