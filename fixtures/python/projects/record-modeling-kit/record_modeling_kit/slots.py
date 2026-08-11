"""Slots, layout, and weak-reference eligibility (PY-CAN-OBJ-009)."""

from __future__ import annotations

import weakref


class SlottedBase:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class SlottedWithDict:
    __slots__ = ("value", "__dict__")

    def __init__(self, value: str) -> None:
        self.value = value
        # Can stash arbitrary attributes via __dict__.
        self.extra = f"extra:{value}"


class SlottedWithWeakref:
    __slots__ = ("label", "__weakref__")

    def __init__(self, label: str) -> None:
        self.label = label


class UnslottedChild(SlottedBase):
    """Unslotted subclass gains __dict__ and __weakref__."""

    pass


class RepeatedSlotDemo:
    pass


def undeclared_assignment_demo() -> str:
    obj = SlottedBase(1, 2)
    try:
        obj.z = 99  # type: ignore[attr-defined]
        return "no-error"
    except AttributeError as exc:
        return f"undeclared:{exc}"


def unslotted_subclass_demo() -> tuple[bool, bool]:
    obj = UnslottedChild(1, 2)
    has_dict = hasattr(obj, "__dict__")
    has_weakref = hasattr(obj, "__weakref__")
    # Can add arbitrary attribute because subclass has dict.
    obj.extra_field = "hello"  # type: ignore[attr-defined]
    return has_dict, has_weakref


def weakref_eligibility_demo() -> tuple[bool, bool]:
    no_weak = SlottedBase(1, 2)
    with_weak = SlottedWithWeakref("ok")
    # SlottedBase has no __weakref__ slot, so weakref should fail.
    try:
        _ = weakref.ref(no_weak)
        weak_no = True
    except TypeError:
        weak_no = False
    try:
        r = weakref.ref(with_weak)
        weak_yes = r() is with_weak
    except TypeError:
        weak_yes = False
    return weak_no, weak_yes


def dict_slot_demo() -> str:
    obj = SlottedWithDict("hello")
    return obj.extra  # type: ignore[attr-defined]


def layout_conflict_demo() -> str:
    class SlotsA:
        __slots__ = ("a",)

    class SlotsB:
        __slots__ = ("b",)

    try:
        class Conflict(SlotsA, SlotsB):  # type: ignore[misc]
            __slots__ = ()

        _ = Conflict
        return "no-layout-conflict"
    except TypeError as exc:
        return f"layout-conflict:{exc}"


def repeated_slot_name_demo() -> str:
    class Dup:
        __slots__ = ("x", "x")  # type: ignore[assignment]

    # On this interpreter duplicate slot names are retained; demonstrate that behavior.
    return f"dup-slots:{Dup.__slots__} count={len(Dup.__slots__)} dedup={len(set(Dup.__slots__))}"


def slot_descriptor_demo() -> str:
    # Slot descriptor lives on class, not instance dict.
    desc = SlottedBase.__dict__["x"]
    return type(desc).__name__
