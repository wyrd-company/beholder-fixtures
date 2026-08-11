"""Static errors versus runtime behavior (PY-CAN-DIAG-007).

Separates checker-negative assignments/overrides/overloads/exhaustiveness
from runtime-negative cases. Checker-negative examples are valid runtime
source without executing a checker; runtime-negative cases run and raise.
"""

from __future__ import annotations

from typing import Any, overload


# ---------------------------------------------------------------------------
# Checker-negative: valid source that a type checker would flag
# ---------------------------------------------------------------------------

# Assignment: int variable assigned a string; checker would flag, runtime is fine.
checker_negative_assignment: int = "mismatch-string"  # type: ignore[assignment]


class CheckerBase:
    """Base with a method that checker-negative overrides break."""

    def handle(self, value: str) -> str:
        return value.upper()


class CheckerNegativeOverride(CheckerBase):
    """Override with incompatible signature – checker variance error, runtime ok."""

    def handle(self, value: int) -> int:  # type: ignore[override]
        return value * 2


@overload
def checker_negative_overload(value: int) -> int: ...


@overload
def checker_negative_overload(value: str) -> str: ...


def checker_negative_overload(value: int | str) -> int | str:
    """Overload stubs plus implementation – missing overload would be checker error."""

    if isinstance(value, int):
        return value * 2
    return value.upper()


def checker_negative_exhaustiveness_demo(value: str) -> str:
    """Match without full exhaustiveness – checker would warn, runtime falls through."""

    match value:
        case "alpha":
            return "A"
        case "beta":
            return "B"
        case _:  # checker exhaustiveness would still want explicit wildcard handling
            return "other"


def checker_negative_any_escape(value: Any) -> int:
    """Any escapes checker analysis – checker-negative but runtime valid."""

    # Using Any silences checker; the assignment is statically allowed but runtime may be wrong.
    result: int = value  # type: ignore[assignment]
    return result


# ---------------------------------------------------------------------------
# Runtime-negative: valid source that raises when executed
# ---------------------------------------------------------------------------


def runtime_negative_assignment() -> dict[str, object]:
    """Runtime type failure from valid source."""

    try:
        # Valid syntax, raises TypeError at runtime.
        _ = "text" + 123  # type: ignore[operator]
        return {"raised": False}
    except TypeError as exc:
        return {"raised": True, "kind": "TypeError", "msg": str(exc)}


def runtime_negative_override_call() -> dict[str, object]:
    """Calling an override with the base-expected type causes runtime failure."""

    obj: CheckerBase = CheckerNegativeOverride()
    try:
        # Checker expects str for CheckerBase.handle, but override expects int.
        # At runtime, passing a string to the int-expecting override still runs,
        # but internal operation may be wrong; trigger via explicit bad type.
        _ = obj.handle(123)  # type: ignore[arg-type]
        # Now try with string which will cause int*str? Actually override does int*2.
        # Passing str will attempt int multiplication but with str it does "abc"*2 = "abcabc" (no error).
        # So trigger a genuine error via overload misuse:
        _ = checker_negative_overload(3.14)  # type: ignore[arg-type]  # float not covered
        return {"raised": False, "value": _}
    except TypeError as exc:
        return {"raised": True, "msg": str(exc)}


def runtime_negative_overload_mismatch() -> dict[str, object]:
    """Call overload with unsupported type – runtime raises."""

    try:
        _ = checker_negative_overload(3.14)  # type: ignore[arg-type]
        # Actually implementation will treat float as str branch and fail on upper()
        return {"raised": False}
    except AttributeError as exc:
        return {"raised": True, "kind": "AttributeError", "msg": str(exc)}
    except TypeError as exc:
        return {"raised": True, "kind": "TypeError", "msg": str(exc)}


def runtime_negative_exhaustiveness_missing_case() -> dict[str, object]:
    """Runtime path that hits an uncovered match arm and raises."""

    def handle_strict(value: str) -> str:
        match value:
            case "alpha":
                return "A"
            case "beta":
                return "B"
            case _:
                raise ValueError(f"unhandled: {value}")

    try:
        _ = handle_strict("gamma")
        return {"raised": False}
    except ValueError as exc:
        return {"raised": True, "kind": "ValueError", "msg": str(exc)}


def runtime_negative_annotation_evaluation_failure() -> dict[str, object]:
    """Annotation evaluated at runtime via typing.get_type_hints may fail."""

    from typing import get_type_hints

    def func_with_bad_annotation(x: "MissingNameXYZ") -> None:  # type: ignore[name-defined]
        pass

    try:
        get_type_hints(func_with_bad_annotation)
        return {"raised": False}
    except NameError as exc:  # annotation evaluation failure
        return {"raised": True, "kind": "NameError", "msg": str(exc)}


def all_static_vs_runtime_demos() -> dict[str, object]:
    """Collect static-vs-runtime demos."""

    return {
        "checker_assignment": checker_negative_assignment,
        "checker_override": CheckerNegativeOverride().handle(21),
        "checker_overload_int": checker_negative_overload(21),
        "checker_overload_str": checker_negative_overload("hi"),
        "checker_exhaustiveness": checker_negative_exhaustiveness_demo("gamma"),
        "checker_any_escape": checker_negative_any_escape("not-an-int"),
        "runtime_type": runtime_negative_assignment(),
        "runtime_overload": runtime_negative_overload_mismatch(),
        "runtime_exhaustiveness": runtime_negative_exhaustiveness_missing_case(),
        "runtime_annotation": runtime_negative_annotation_evaluation_failure(),
    }
