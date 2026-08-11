"""Nominal new types and narrowing predicates (PY-CAN-TYPE-012)."""

from __future__ import annotations

from typing import NewType, TypeGuard, TypeIs

# --- NewType: identity-like runtime value ------------------------------------

InventoryId = NewType("InventoryId", int)
BatchId = NewType("BatchId", str)
UserId = NewType("UserId", int)


def newtype_runtime_demo() -> dict[str, object]:
    raw = 42
    typed: InventoryId = InventoryId(raw)
    return {
        "is_int": isinstance(typed, int),
        "value": typed,
        "same_object": typed is raw,  # NewType is identity at runtime in CPython
        "callable": callable(InventoryId),
    }


def newtype_unsound_demo(value: InventoryId) -> int:
    # NewType is not a real class: ``isinstance`` checks against underlying type.
    return value + 1


# --- TypeGuard: positive-only narrowing ---------------------------------------

def is_str(value: object) -> TypeGuard[str]:
    return isinstance(value, str)


def is_batch_id(value: object) -> TypeGuard[BatchId]:
    return isinstance(value, str) and value.startswith("batch-")


def typeguard_positive_only_demo(value: object) -> str:
    if is_str(value):
        # Checker narrows ``value`` to ``str`` in this branch only
        return value.upper()
    # Outside the ``if``, ``value`` remains ``object``
    return str(value)


def typeguard_unsound_predicate(value: object) -> TypeGuard[str]:
    # Unsound predicate: claims to narrow but returns True incorrectly
    return True


# --- TypeIs: two-branch narrowing (Python 3.13+) ------------------------------

def is_inventory_id(value: object) -> TypeIs[InventoryId]:
    return isinstance(value, int) and value > 0


def typeis_two_branch_demo(value: object) -> str:
    if is_inventory_id(value):
        # Checker narrows to ``InventoryId`` in the ``if`` branch
        return f"id:{value}"
    else:
        # Checker narrows to ``object`` excluding ``InventoryId`` in the ``else`` branch
        return f"not-id:{value!r}"


def typeguard_vs_typeis_demo(value: int | str) -> str:
    # TypeGuard narrows only in the positive branch; TypeIs narrows in both.
    if is_str(value):
        positive: str = value
        return positive
    # ``value`` is still ``int | str`` after TypeGuard failure branch (positive-only)
    return str(value)


def typeis_both_branches(value: int | str) -> str:
    # Using TypeIs: both branches are narrowed
    def is_int_str_guard(v: object) -> TypeIs[str]:
        return isinstance(v, str)

    if is_int_str_guard(value):
        narrowed_str: str = value
        return narrowed_str
    else:
        narrowed_int: int = value  # type: ignore[assignment]
        return str(narrowed_int)


# --- Subtype requirement variant ----------------------------------------------

class Tag:
    label: str

    def __init__(self, label: str) -> None:
        self.label = label


class SpecialTag(Tag):
    extra: str

    def __init__(self, label: str, extra: str) -> None:
        super().__init__(label)
        self.extra = extra


def is_special_tag(value: Tag) -> TypeIs[SpecialTag]:
    return isinstance(value, SpecialTag)


def subtype_requirement_demo(value: Tag) -> str:
    if is_special_tag(value):
        return value.extra
    return value.label
