"""Control-flow narrowing and exhaustiveness (PY-CAN-TYPE-020)."""

from __future__ import annotations

from typing import Any, Literal, TypedDict, assert_never

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


def narrow_via_assertion(value: int | str | None) -> str:
    # Genuinely narrowing assertion: asserts one constituent of the union.
    assert isinstance(value, str)
    # After the assertion, checker narrows ``value`` to ``str``.
    return value.upper()


def narrow_via_predicate(value: object) -> str:
    if is_str(value):
        return value.upper()
    return str(value)


# --- Discriminated union variant ----------------------------------------------

class BatchKind(TypedDict):
    kind: Literal["batch"]
    label: str
    quantity: int


class RecordKind(TypedDict):
    kind: Literal["record"]
    value: int
    note: str


Item = BatchKind | RecordKind


def narrow_via_discriminant(item: Item) -> str:
    # Branching on the literal ``kind`` discriminant narrows the union.
    if item["kind"] == "batch":
        # ``item`` narrowed to ``BatchKind`` exposing ``label``.
        return item["label"]
    else:
        # ``item`` narrowed to ``RecordKind`` exposing ``value``.
        return str(item["value"])


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
# Narrowing a mutable member expression (not a copied local) and then mutating
# through an alias so the checker must invalidate the prior narrowing.

class Holder:
    def __init__(self, value: int | str) -> None:
        self.value: int | str = value


def mutation_invalidation_demo(holder: Holder, alias: Holder) -> str:
    # Narrow the member expression ``holder.value``.
    if isinstance(holder.value, str):
        # Mutate through alias that may point to the same object.
        alias.value = 42
        # Checker can no longer assume ``holder.value`` is still ``str``.
        # At runtime, if ``holder is alias``, the mutation affects holder.
        return f"narrowed_was_str:{holder.value!r} alias_is_same:{holder is alias}"
    return f"was_int:{holder.value!r}"


def alias_invalidation_demo(holder: Holder) -> str:
    # Narrow ``holder.value`` then mutate via alias dict-style access through
    # ``holder`` vs separate reference is not needed; we use a second holder alias.
    other = holder
    if isinstance(holder.value, str):
        other.value = 99
        # ``holder.value`` might now be int if ``other is holder``.
        return f"after:{holder.value!r}"
    return str(holder.value)


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
