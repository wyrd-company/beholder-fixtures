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


# Union variant: annotation-inferred union and explicit union registration.
@format_value.register
def _format_bytes_union(value: bytes | bytearray) -> str:
    return f"bytes:{len(value)}"


# Explicit union type registration (Union syntax) — covers list and tuple jointly.
@format_value.register(Union[list, tuple])
def _format_list_tuple_union(value: list | tuple) -> str:
    return f"list-tuple-union:{len(value)}"


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


# Extra abstract-base registrations: an instance of a registered ABC dispatches
# to the ABC handler when no concrete registration is more specific.
@format_value.register(cabc.Hashable)
def _format_hashable(value: cabc.Hashable) -> str:
    return f"hashable:{hash(value) % 1000}"


@format_value.register(cabc.Sized)
def _format_sized(value: cabc.Sized) -> str:
    return f"sized:{len(value)}"


def ambiguous_abc_pair() -> tuple[object, str]:
    """Show genuine implicit-ABC ambiguity and its explicit resolution.

    ``Iterable`` and ``Container`` are unrelated ABCs — neither is a structural
    subclass of the other. A class defining ``__iter__`` and ``__contains__`` is
    a *virtual* subclass of both without inheriting either, so it appears in the
    dispatch MRO under both with equal specificity. ``functools`` refuses to
    guess and raises ``RuntimeError("Ambiguous dispatch: ...")`` until the
    concrete class is registered explicitly.

    A dedicated dispatcher keeps the ambiguity isolated from ``format_value``.
    """

    @singledispatch
    def classify(value: object) -> str:
        return "default"

    @classify.register(cabc.Iterable)
    def _classify_iterable(value: cabc.Iterable) -> str:
        return "iterable"

    @classify.register(cabc.Container)
    def _classify_container(value: cabc.Container) -> str:
        return "container"

    class IterableContainer:
        def __iter__(self) -> "object":
            return iter(())

        def __contains__(self, item: object) -> bool:
            return False

    inst = IterableContainer()
    try:
        classify.dispatch(type(inst))
    except RuntimeError as exc:
        before = f"ambiguous:{type(exc).__name__}"
    else:
        before = "resolved"

    @classify.register(IterableContainer)
    def _classify_both(value: IterableContainer) -> str:  # type: ignore[no-redef]
        return "both"

    after = classify.dispatch(type(inst)).__name__
    return inst, f"{before}->{after}"


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
