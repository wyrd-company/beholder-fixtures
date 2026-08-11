"""Annotation evaluation regimes (PY-CAN-TYPE-001).

Covers future-stringized annotations via ``from __future__ import annotations``,
the deferred annotation regime that is the default on CPython 3.14 (PEP 649),
raw-versus-resolved hint inspection, and the excluded eager regime as context.
"""

from __future__ import annotations

import typing
from typing import get_type_hints

# --- Forward name variant ----------------------------------------------------
# The referenced name is used before it is defined, exercising a true
# forward reference under postponed evaluation.

def create_batch(label: str) -> Batch:
    return Batch(label)  # type: ignore[name-defined]


class Batch:
    """A simple batch record referenced before its definition above."""

    def __init__(self, label: str = "") -> None:
        self.label = label


# --- Side-effectful annotation expression variant ----------------------------

_side_effect_calls: list[str] = []


def _side_effect() -> type:
    _side_effect_calls.append("evaluated")
    return int


# Under ``from __future__ import annotations`` the call ``_side_effect()``
# inside the annotation is stringized and not evaluated at definition time.
def with_side_effect(value: _side_effect()) -> _side_effect():  # type: ignore[valid-type]
    return value


def side_effect_not_yet_evaluated() -> bool:
    # If the annotation had been eager, _side_effect() would have run.
    raw = with_side_effect.__annotations__["value"]
    return isinstance(raw, str) and len(_side_effect_calls) == 0


def side_effect_annotation() -> list[str]:
    """Legacy helper keeps import compatibility; no longer claims side effect."""

    def _helper(items: list[str] = []) -> list[str]:  # noqa: B006
        return items

    return _helper()


# Demonstrate side-effectful annotation with a forward reference to a yet-undefined
# alias.  The expression is not evaluated at definition time under postponed
# evaluation.
def deferred_side_effect(value: "Counter") -> "Counter":
    return value


class Counter:
    count: int


# --- Local and class scope variant ------------------------------------------

def class_scope_annotations() -> tuple[dict, dict]:
    class Record:
        items: list[str]
        count: int = 0

        def method(self, value: str) -> str:
            local_var: int = 42
            return value

    return Record.__annotations__, Record.method.__annotations__


def local_scope_annotations(flag: bool) -> dict:
    if flag:
        x: int = 1
    else:
        x: str = "fallback"
    # Local annotations are not retained on the function object at runtime;
    # they are compiler-classified but not stored in __annotations__.
    return locals()


# --- Raw versus resolved hint inspection ------------------------------------

class InventoryItem:
    label: str
    quantity: int


def raw_annotations_demo() -> dict[str, object]:
    """Return raw ``__annotations__`` (stringized under future import)."""
    return InventoryItem.__annotations__


def resolved_hints_demo() -> dict[str, object]:
    """Return resolved hints via ``get_type_hints``."""
    return get_type_hints(InventoryItem)


def missing_resolution_namespace() -> tuple[str, str]:
    """Attempt to resolve hints with missing namespace produces error."""

    def _inner(value: "UndefinedName") -> "UndefinedName":  # noqa: F821
        return value  # type: ignore[return]

    raw = _inner.__annotations__["value"]
    try:
        get_type_hints(_inner)
        result = "resolved"
    except NameError as exc:
        result = f"NameError:{exc}"
    return raw, result  # type: ignore[return]


# --- Later runtime consumer variant -----------------------------------------

def consume_later(obj: InventoryItem) -> str:
    hints = get_type_hints(InventoryItem)
    if hints.get("label") is str:
        return obj.label
    return ""


# --- Deferred default regime note (3.14) ------------------------------------

# On CPython 3.14 the default is deferred annotations (PEP 649 / PEP 749).
# ``from __future__ import annotations`` preserves the stringized opt-in
# behaviour for this module.  Without that import, annotations are stored
# as deferred evaluation objects accessible via ``annotationlib`` rather
# than eagerly evaluated at class/function definition time.  The eager
# definition-time regime of Python 3.13 and earlier is not available on
# 3.14 and is therefore an excluded historical-interpreter variant.

def annotation_format_demo() -> str:
    """Return the string form of annotations to show stringized storage."""
    return InventoryItem.__annotations__["label"]  # type: ignore[return]


def stringized_raw_check() -> bool:
    """Verify raw annotations are strings under future-stringized regime."""
    return isinstance(InventoryItem.__annotations__["label"], str)
