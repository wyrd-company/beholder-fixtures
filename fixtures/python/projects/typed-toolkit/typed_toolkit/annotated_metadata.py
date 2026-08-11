"""Annotated metadata (PY-CAN-TYPE-019)."""

from __future__ import annotations

from typing import Annotated, get_type_hints, get_origin, get_args
from dataclasses import dataclass

# --- Annotated metadata definitions -------------------------------------------

class Unit:
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"Unit({self.name!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Unit) and self.name == other.name


class Range:
    def __init__(self, low: float, high: float) -> None:
        self.low = low
        self.high = high

    def __repr__(self) -> str:
        return f"Range({self.low},{self.high})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Range) and self.low == other.low and self.high == other.high


UnitAnnotation = Annotated[int, Unit("pcs")]
RangedInt = Annotated[int, Range(0, 100), Unit("items")]

# Ordered, repeated metadata
MultiMeta = Annotated[str, "first", "second", "first"]


# --- Preserve ordered, repeated metadata through hint resolution ---------------

class Batch:
    count: Annotated[int, Unit("pcs"), Range(0, 1000)]
    label: Annotated[str, "indexed", "searchable"]
    repeated: Annotated[str, "a", "b", "a"]


def preserve_ordered_metadata_demo() -> dict[str, tuple[object, ...]]:
    hints = get_type_hints(Batch, include_extras=True)
    return {
        "count": get_args(hints["count"])[1:],
        "label": get_args(hints["label"])[1:],
        "repeated": get_args(hints["repeated"])[1:],
    }


def extras_stripped_unless_requested_demo() -> dict[str, object]:
    without = get_type_hints(Batch, include_extras=False)
    with_extras = get_type_hints(Batch, include_extras=True)
    return {
        "without_extras_count": without["count"],
        "with_extras_count": with_extras["count"],
        "stripped_is_int": without["count"] is int,
    }


# --- Alias boundary variant: non-flattening PEP 695 TypeAliasType -------------
# A PEP 695 ``type`` statement creates a genuine ``TypeAliasType`` object rather
# than an ordinary runtime assignment.  Nesting one alias inside ``Annotated``
# keeps the inner alias as a distinct boundary: ``AliasedQuantity.__value__`` is
# ``Annotated[Quantity, Range(0, 500)]`` whose first argument is the ``Quantity``
# alias object, not the flattened ``int``.  An ordinary assignment alias would
# instead flatten to ``Annotated[int, Unit("kg"), Range(0, 500)]`` -- the boundary
# lost.  Inspect ``__value__`` to observe the preserved alias boundary.

type Quantity = Annotated[int, Unit("kg")]
type AliasedQuantity = Annotated[Quantity, Range(0, 500)]


class AliasedHolder:
    direct: Quantity
    wrapped: AliasedQuantity


def alias_flattening_demo() -> dict[str, object]:
    # Resolving the holder's annotations yields the ``TypeAliasType`` objects
    # themselves -- the alias boundary survives at the class level too.
    hints = get_type_hints(AliasedHolder, include_extras=True)
    outer = get_args(AliasedQuantity.__value__)
    inner = get_args(Quantity.__value__)
    return {
        "direct_resolves_to_alias": hints["direct"] is Quantity,
        "wrapped_resolves_to_alias": hints["wrapped"] is AliasedQuantity,
        "wrapped_value_args": outer,
        "wrapped_first_is_quantity": outer[0] is Quantity,
        "wrapped_first_is_int": outer[0] is int,
        "quantity_value_args": inner,
    }


def alias_boundary_preserved() -> bool:
    # Non-flattening proof: the outer alias value keeps the inner ``Quantity``
    # alias as its first argument instead of collapsing to ``int``.
    outer = get_args(AliasedQuantity.__value__)
    inner = get_args(Quantity.__value__)
    return outer[0] is Quantity and outer[0] is not int and inner[0] is int


# --- Order-sensitive equality variant -----------------------------------------

def order_sensitive_equality_demo() -> dict[str, bool]:
    a = Annotated[int, "x", "y"]
    b = Annotated[int, "y", "x"]
    c = Annotated[int, "x", "y"]
    return {
        "a_eq_c": a == c,
        "a_ne_b": a != b,
        "same_order_equal": Annotated[int, Unit("a")] != Annotated[int, Unit("b")],
    }


# --- Runtime consumer variant -------------------------------------------------

def consume_metadata(hint: object) -> list[object]:
    """Extract metadata from an Annotated hint at runtime."""
    if get_origin(hint) is Annotated:
        return list(get_args(hint)[1:])
    return []


def runtime_consumer_demo() -> list[object]:
    hints = get_type_hints(Batch, include_extras=True)
    return consume_metadata(hints["count"])


def incompatible_consumer_demo() -> str:
    # Two consumers interpret the same metadata differently (e.g., Unit vs Range)
    hints = get_type_hints(Batch, include_extras=True)
    meta = consume_metadata(hints["count"])
    units = [m for m in meta if isinstance(m, Unit)]
    ranges = [m for m in meta if isinstance(m, Range)]
    return f"units:{len(units)} ranges:{len(ranges)}"
