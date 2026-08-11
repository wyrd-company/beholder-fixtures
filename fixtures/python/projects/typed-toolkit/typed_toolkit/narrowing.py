"""Control-flow narrowing and exhaustiveness (PY-CAN-TYPE-020)."""

from __future__ import annotations

from typing import Any, Literal, assert_never

from typed_toolkit.narrowing_predicates import is_str, is_inventory_id

# --- Union to narrow ----------------------------------------------------------

NumberOrText = int | str


def narrow_via_conditions(value: int | str | None) -> str:
    if value is None:
        return "none"
    if isinstance(value, int):
        return f"int:{value}"
    return f"str:{value}"


def narrow_via_isinstance(value: object) -> str:
    if isinstance(value, str):
        return value.upper()
    if isinstance(value, int):
        return str(value * 2)
    return repr(value)


def narrow_via_assertion(value: int | str) -> str:
    assert isinstance(value, str) or isinstance(value, int)
    if isinstance(value, str):
        return value
    return str(value)


def narrow_via_predicate(value: object) -> str:
    if is_str(value):
        return value.upper()
    return str(value)


def narrow_via_discriminant(batches: list[dict[str, object]]) -> str:
    # Discriminant via literal key ``kind``
    for item in batches:
        if item.get("kind") == "batch":
            return str(item.get("label"))
    return "empty"


def narrow_via_typeis(value: object) -> str:
    if is_inventory_id(value):
        return f"id:{value}"
    return f"other:{value!r}"


def narrow_via_match(value: int | str | None) -> str:
    match value:
        case None:
            return "none"
        case int(n):
            return f"int:{n}"
        case str(s):
            return f"str:{s}"
        case _:
            assert_never(value)


# --- Exhaustiveness with assert_never ----------------------------------------

Status = Literal["pending", "active", "closed"]


def exhaustive_status(status: Status) -> str:
    if status == "pending":
        return "wait"
    elif status == "active":
        return "go"
    elif status == "closed":
        return "done"
    else:
        assert_never(status)


# --- Mutation and alias invalidation variant ---------------------------------

def mutation_invalidation_demo(values: list[int | str]) -> str:
    # Checker would invalidate narrowing after mutation; runtime shows the effect.
    x: int | str = values[0] if values else 0
    if isinstance(x, str):
        values[0] = 42  # mutation through alias
        # After mutation, ``x`` is still str, but ``values[0]`` is int
        return f"was_str:{x} now:{values[0]!r}"
    return f"was_int:{x}"


def alias_invalidation_demo() -> str:
    data: dict[str, int | str] = {"key": "hello"}
    alias = data
    value = data["key"]
    if isinstance(value, str):
        alias["key"] = 99
        # ``value`` remains str even though dict entry changed
        return value.upper()
    return str(value)


# --- Negative checks variant --------------------------------------------------

def negative_checks(value: int | str | None) -> str:
    if value is not None and not isinstance(value, int):
        # Narrowed to str after excluding None and int
        return value.upper()  # type: ignore[union-attr]
    if value is None:
        return "none"
    return str(value)


# --- Any variant --------------------------------------------------------------

def any_bypasses_narrowing(value: Any) -> str:
    if isinstance(value, str):
        return value.upper()
    # ``Any`` is compatible with all types; checker may not narrow strictly
    return str(value)


# --- Checker-dependent exhaustiveness note -----------------------------------

# Exhaustiveness via ``assert_never`` relies on the checker enumerating all
# union members.  At runtime ``assert_never`` simply raises ``AssertionError``
# for any value.

def checker_dependent_exhaustiveness(value: Status) -> str:
    match value:
        case "pending":
            return "p"
        case "active":
            return "a"
        case "closed":
            return "c"
        case _:
            assert_never(value)
