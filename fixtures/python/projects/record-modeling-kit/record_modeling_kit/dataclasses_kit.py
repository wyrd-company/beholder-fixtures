"""Dataclass-generated fields and methods (PY-CAN-OBJ-013)."""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import ClassVar, Final


# Basic dataclass with defaults, factories, ClassVar, InitVar.
@dataclass
class BaseItem:
    name: str
    count: int = 0
    tags: list[str] = field(default_factory=list)
    kind: ClassVar[str] = "base"
    extra: dataclasses.InitVar[str | None] = None

    def __post_init__(self, extra: str | None) -> None:
        if extra is not None:
            self.tags.append(extra)


@dataclass
class DerivedItem(BaseItem):
    priority: int = 1


# Frozen, keyword-only, slots, matching, hashing.
@dataclass(frozen=True, slots=True)
class FrozenItem:
    label: str
    score: int = 0


@dataclass(kw_only=True)
class KwOnlyItem:
    a: int
    b: int = 10
    c: str = "default"


@dataclass(slots=True)
class SlottedItem:
    x: int
    y: int
    note: str = "slotted"

    def move(self, dx: int, dy: int) -> SlottedItem:
        return SlottedItem(self.x + dx, self.y + dy, self.note)


@dataclass(frozen=True, unsafe_hash=True)
class HashableMutable:
    # frozen historically hashable; unsafe_hash allows hashing even if not frozen? demo both.
    items: tuple[int, ...] = ()


def dataclass_defaults_demo() -> BaseItem:
    a = BaseItem("alpha")
    b = BaseItem("beta", tags=["pre"])
    a.tags.append("extra")
    # Ensure factories are not shared.
    assert b.tags == ["pre"]
    return a


def inheritance_demo() -> DerivedItem:
    return DerivedItem("derived", count=2, priority=5, extra="note")


def frozen_demo() -> str:
    item = FrozenItem("f", score=3)
    try:
        item.score = 4  # type: ignore[misc]
        return "no-error"
    except dataclasses.FrozenInstanceError as exc:
        return f"frozen-error:{exc}"


def kw_only_demo() -> KwOnlyItem:
    return KwOnlyItem(a=1, b=2, c="kw")


def slots_demo() -> bool:
    obj = SlottedItem(1, 2)
    has_dict = hasattr(obj, "__dict__")
    # Slotted dataclass should not have __dict__ by default.
    moved = obj.move(3, 4)
    return (not has_dict) and moved.x == 4


def matching_demo(match_obj: BaseItem | FrozenItem | SlottedItem) -> str:
    match match_obj:
        case BaseItem(name="alpha"):
            return "alpha"
        case FrozenItem(label=lab):
            return f"frozen:{lab}"
        case SlottedItem(x=1, y=2):
            return "slotted-1-2"
        case BaseItem(name=name):
            return f"base:{name}"
        case _:
            return "other"


def hashing_demo() -> tuple[int, int, bool]:
    f1 = FrozenItem("h", 1)
    f2 = FrozenItem("h", 1)
    hm = HashableMutable((1, 2))
    # Same-type equality: FrozenItem("h",1) == FrozenItem("h",1) but not equal to unsafe hash type.
    same_type_eq = f1 == f2
    return hash(f1), hash(hm), same_type_eq


def same_type_equality_demo() -> bool:
    # Dataclass equality requires same type.
    a = BaseItem("x")
    b = DerivedItem("x")
    return a == b  # False because types differ


def mutable_default_rejection_demo() -> str:
    try:
        @dataclass
        class Bad:
            items: list[int] = []  # type: ignore[assignment]

        _ = Bad
        return "no-error"
    except ValueError as exc:
        return f"mutable-default:{exc}"


def field_order_failure_demo() -> str:
    try:
        @dataclass
        class BadOrder:
            with_default: int = 1
            without_default: int  # type: ignore[assignment]

        _ = BadOrder
        return "no-error"
    except TypeError as exc:
        return f"field-order:{exc}"


def descriptor_default_demo() -> str:
    class DescDefault:
        def __get__(self, instance: object | None, owner: type | None = None) -> str:
            if instance is None:
                return "desc-class"
            return "desc-instance"

    @dataclass
    class WithDesc:
        name: str = field(default="from-field")
        # Field with descriptor-like default probe.
        probe: str = "value"

    obj = WithDesc()
    return obj.probe


def post_init_demo() -> BaseItem:
    return BaseItem("post", extra="added")


def replacement_under_slots_demo() -> str:
    # Slots dataclass replaces class with new type that has __slots__.
    return type(SlottedItem).__name__
