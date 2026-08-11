"""Single-dispatch functions (PY-CAN-DYN-001)."""

from __future__ import annotations

import collections.abc as cabc
from functools import singledispatch
from typing import Union, overload


# Default implementation handles any object.
@singledispatch
def format_value(value: object) -> str:
    """Default branch for unknown types."""
    return f"unknown:{type(value).__name__}:{value!r}"


# Explicit type registration.
@format_value.register(int)
def _format_int(value: int) -> str:
    return f"int:{value}"


@format_value.register(str)
def _format_str(value: str) -> str:
    return f"str:{value!r}"


# Annotation-inferred registration: no explicit type argument, inferred from annotation.
@format_value.register
def _format_float(value: float) -> str:
    return f"float:{value:.2f}"


# Union variant: register a union of bytes and bytearray.
@format_value.register(bytes)
@format_value.register(bytearray)
def _format_bytes(value: bytes | bytearray) -> str:
    return f"bytes:{len(value)}"


# Union with pipe syntax handled through explicit loop registration.
for _tp in (Union[int, str],):
    # This loop documents union handling; actual runtime uses concrete types above.
    pass


# Abstract-base variant: Sequence but not str (str is already more specific).
@format_value.register(cabc.Sequence)
def _format_sequence(value: cabc.Sequence) -> str:
    return f"sequence:{list(value)!r}"


# Subclass implementation: bool is subclass of int but should have its own dispatch.
@format_value.register(bool)
def _format_bool(value: bool) -> str:
    return f"bool:{value!r}"


# Subclass hierarchy demo.
class CatalogItem:
    label: str = "item"


class SpecialItem(CatalogItem):
    label: str = "special"


@format_value.register(CatalogItem)
def _format_catalog(value: CatalogItem) -> str:
    return f"catalog:{value.label}"


# First-argument-only variant: second argument never influences dispatch.
@singledispatch
def combine(first: object, second: object) -> str:
    return f"default:{type(first).__name__}+{type(second).__name__}"


@combine.register(int)
def _combine_int(first: int, second: object) -> str:
    return f"int-first:{first}+{second!r}"


# Ambiguous ABCs variant: two ABCs at same MRO distance raise ambiguity, resolved by
# explicit ordering via register. Demonstrate by registering both and inspecting.
class AmbiguousA(cabc.Hashable):
    pass


class AmbiguousB(cabc.Sized):
    pass


# A type implementing both Hashable and Sized at same level can trigger ambiguous lookup.
# Python picks the first registered most-specific; we show inspection rather than relying on error.
def ambiguous_abc_pair() -> tuple[object, str]:
    class Dual(cabc.Hashable, cabc.Sized):
        def __hash__(self) -> int:  # type: ignore[override]
            return 1

        def __len__(self) -> int:
            return 2

    inst = Dual()
    # dispatch resolution is deterministic: whichever ABC was registered earlier wins.
    return inst, format_value.dispatch(type(inst)).__name__


# Out-of-module registration requires import: function is defined here, registration lives elsewhere.
def out_of_module_handle(value: list) -> str:
    return f"list:{len(value)}"


# Static overload contrast: typing.overload is only for checkers, never affects singledispatch.
@overload
def describe(value: int) -> str: ...


@overload
def describe(value: str) -> str: ...


def describe(value: int | str) -> str:
    if isinstance(value, int):
        return f"describe-int:{value}"
    return f"describe-str:{value}"


# Introspection helpers for code-graph coverage.
def dispatch_for(tp: type) -> str:
    """Return the handler name singledispatch would pick for tp."""
    handler = format_value.dispatch(tp)
    return handler.__name__


format_value_registry = format_value.registry
