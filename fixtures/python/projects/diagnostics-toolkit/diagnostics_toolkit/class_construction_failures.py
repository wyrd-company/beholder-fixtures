"""Class-construction failures (PY-CAN-DIAG-020).

Isolates inconsistent MRO, metaclass conflict, duplicate base,
and slot/layout conflict as runtime class-construction failures
from valid, parseable source.
"""

from __future__ import annotations


def demo_inconsistent_mro() -> dict[str, object]:
    """Inconsistent MRO – C3 linearization failure."""

    class A:
        pass

    class B(A):
        pass

    class C(A):
        pass

    # Classic inconsistent hierarchy: D inherits from B and C where order conflicts
    # Use a more explicit inconsistency: class X, class Y, class Z(X,Y), class W(Y,X), class Bad(Z,W)
    class X:
        pass

    class Y:
        pass

    class Z(X, Y):
        pass

    class W(Y, X):
        pass

    try:

        class Bad(Z, W):  # type: ignore[type-arg]
            pass

        return {"raised": False, "mro": Bad.__mro__}
    except TypeError as exc:
        return {"raised": True, "kind": "TypeError", "msg": str(exc), "mro_failed": True}


def demo_metaclass_conflict() -> dict[str, object]:
    """Metaclass conflict – bases have incompatible metaclasses."""

    class MetaOne(type):
        pass

    class MetaTwo(type):
        pass

    class BaseOne(metaclass=MetaOne):
        pass

    class BaseTwo(metaclass=MetaTwo):
        pass

    try:

        class Conflict(BaseOne, BaseTwo):  # type: ignore[misc]
            pass

        return {"raised": False}
    except TypeError as exc:
        return {"raised": True, "kind": "TypeError", "msg": str(exc)}


def demo_duplicate_base() -> dict[str, object]:
    """Duplicate base class – same base listed twice."""

    class Base:
        pass

    try:

        class Dupe(Base, Base):  # type: ignore[misc]
            pass

        return {"raised": False}
    except TypeError as exc:
        return {"raised": True, "kind": "TypeError", "msg": str(exc)}


def demo_slot_layout_conflict() -> dict[str, object]:
    """Slot/layout conflict – incompatible slot layouts."""

    class SlottedA:
        __slots__ = ("x",)

    class SlottedB:
        __slots__ = ("y",)

    # Combining slots from unrelated bases with slots can fail if layout incompatible.
    # Use a more direct conflict: non-empty slots with duplicate slot name or
    # mixing with a base that has __slots__ and a base that uses __dict__ incompatibly.
    # CPython reports layout conflict for certain combinations:
    # e.g., two slotted bases where one has a slot with same name as the other.
    class WithSlotX:
        __slots__ = ("x",)

    class AlsoWithSlotX:
        __slots__ = ("x",)

    try:

        class SlotConflict(WithSlotX, AlsoWithSlotX):  # type: ignore[misc]
            pass

        return {"raised": False, "mro": [c.__name__ for c in SlotConflict.__mro__]}
    except TypeError as exc:
        return {"raised": True, "kind": "TypeError", "msg": str(exc)}

    # Alternative demonstration for non-empty __slots__ conflict – also try
    # a class inheriting from a slotted class and a non-slotted with __slots__ mismatch.
    # The above already covers the variant; the second path is unreachable if first raises.


def demo_slot_dup_in_single_class() -> dict[str, object]:
    """Duplicate slot name inside one class – immediate TypeError."""

    try:

        class BadSlots:
            __slots__ = ("a", "a")  # type: ignore[misc]

        _ = BadSlots
        return {"raised": False}
    except (TypeError, ValueError) as exc:
        return {"raised": True, "kind": type(exc).__name__, "msg": str(exc)}


def all_class_construction_demos() -> dict[str, object]:
    """Collect class-construction failure demos."""

    return {
        "inconsistent_mro": demo_inconsistent_mro(),
        "metaclass_conflict": demo_metaclass_conflict(),
        "duplicate_base": demo_duplicate_base(),
        "slot_layout": demo_slot_layout_conflict(),
        "slot_duplicate": demo_slot_dup_in_single_class(),
    }
