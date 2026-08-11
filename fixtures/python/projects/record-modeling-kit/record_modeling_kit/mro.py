"""Multiple inheritance and C3 MRO (PY-CAN-OBJ-003)."""

from __future__ import annotations

import abc


class DiamondBase:
    def handle(self) -> str:
        return "base"


class DiamondLeft(DiamondBase):
    def handle(self) -> str:
        return f"left->{super().handle()}"


class DiamondRight(DiamondBase):
    def handle(self) -> str:
        return f"right->{super().handle()}"


class DiamondLeaf(DiamondLeft, DiamondRight):
    """Diamond with cooperative overrides; inspect linearization."""

    def handle(self) -> str:
        return f"leaf->{super().handle()}"


def mro_names(cls: type) -> list[str]:
    return [c.__name__ for c in cls.__mro__]


def mro_linearization_demo() -> list[str]:
    return mro_names(DiamondLeaf)


def base_order_change_demo() -> tuple[list[str], list[str]]:
    class LeafA(DiamondLeft, DiamondRight):
        pass

    class LeafB(DiamondRight, DiamondLeft):
        pass

    return mro_names(LeafA), mro_names(LeafB)


def inconsistent_hierarchy_demo() -> str:
    class A(DiamondLeft, DiamondRight):
        pass

    class B(DiamondRight, DiamondLeft):
        pass

    try:
        class Inconsistent(A, B):  # type: ignore[misc]
            pass

        return "no-error"
    except TypeError as exc:
        return f"inconsistent-mro:{exc}"


def virtual_subclass_absent_demo() -> tuple[bool, bool, bool, list[str]]:
    class VirtualBase(abc.ABC):
        @abc.abstractmethod
        def action(self) -> str: ...

    class VirtualImpl:
        def action(self) -> str:
            return "virtual"

    VirtualBase.register(VirtualImpl)
    impl = VirtualImpl()
    is_virtual = isinstance(impl, VirtualBase)
    is_sub = issubclass(VirtualImpl, VirtualBase)
    # Virtual subclass is absent from implementation MRO; registered base not in impl MRO.
    absent_from_impl = VirtualBase not in VirtualImpl.__mro__
    return is_virtual, is_sub, absent_from_impl, [c.__name__ for c in VirtualImpl.__mro__]


def extension_layout_conflict_demo() -> str:
    # Two slotted bases with incompatible layout can raise TypeError.
    class SlotsA:
        __slots__ = ("a",)

    class SlotsB:
        __slots__ = ("b",)

    try:
        class Conflict(SlotsA, SlotsB):  # type: ignore[misc]
            __slots__ = ()

        _ = Conflict
        return "layout-allowed"
    except TypeError as exc:
        return f"layout-conflict:{exc}"


def cooperative_super_demo() -> str:
    return DiamondLeaf().handle()
