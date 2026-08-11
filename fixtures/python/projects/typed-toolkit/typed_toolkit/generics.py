"""Generic classes/functions and runtime erasure (PY-CAN-TYPE-006)."""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")
K = TypeVar("K")
V = TypeVar("V")

# --- Old syntax generics ------------------------------------------------------

class OldBox(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value


def old_identity(value: T) -> T:
    return value


# --- New syntax generics (PEP 695, Python 3.12+) -----------------------------

class NewBox[T]:
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value


def new_identity[T](value: T) -> T:
    return value


# --- Specialization and instantiation ----------------------------------------

def specialize_demo() -> tuple[OldBox[int], NewBox[str]]:
    a: OldBox[int] = OldBox(42)
    b: NewBox[str] = NewBox("hello")
    # At runtime ``OldBox[int]`` and ``OldBox[str]`` are the same object.
    return a, b


def same_runtime_class_demo() -> bool:
    # Generic aliases are distinct objects, but the runtime class of instances
    # is the same; the origin is shared.  Erasure is demonstrated by instance
    # type identity and shared __origin__.
    return type(OldBox(1)) is type(OldBox("x")) and OldBox[int].__origin__ is OldBox  # type: ignore[attr-defined]


# --- Best-effort __orig_class__ ------------------------------------------------

def orig_class_demo() -> object | None:
    box = OldBox(123)
    # CPython stashes the subscripted alias on the instance when Generic is
    # instantiated via ``__orig_class__`` (best-effort, not guaranteed for
    # all generics).
    box.__orig_class__ = OldBox[int]  # type: ignore[attr-defined]
    return getattr(box, "__orig_class__", None)


# --- Runtime metadata inspection ----------------------------------------------

def runtime_metadata_demo() -> dict[str, object]:
    return {
        "old_box_type_params": getattr(OldBox, "__type_params__", None),
        "new_box_type_params": getattr(NewBox, "__type_params__", None),
        "old_box_args": getattr(OldBox[int], "__args__", None),  # type: ignore[attr-defined]
    }


# --- Metaclass conflict variant -----------------------------------------------

class MetaA(type):
    pass


class MetaB(type):
    pass


def metaclass_conflict_demo() -> str:
    try:
        class Conflicted(Generic[T], metaclass=MetaA):  # type: ignore[type-var]
            pass

        class AlsoConflicted(Generic[T], metaclass=MetaB):  # type: ignore[type-var]
            pass

        # Combining bases with different metaclasses would conflict in a diamond.
        class Diamond(Conflicted[int], AlsoConflicted[str]):  # type: ignore[misc]
            pass
        return "no-conflict"
    except TypeError as exc:
        return f"TypeError:{exc}"


# --- Partial and full subclass specialization ---------------------------------

class PartialSpecialization(OldBox[int]):
    pass


class FullSpecialization(NewBox[str]):
    def greeting(self) -> str:
        return f"hello:{self.get()}"


class GenericSubclass[T, U]:
    def __init__(self, first: T, second: U) -> None:
        self.first = first
        self.second = second


class PartialGenericSubclass(GenericSubclass[int, str]):
    pass


def subclass_specialization_demo() -> tuple[PartialSpecialization, FullSpecialization]:
    return PartialSpecialization(10), FullSpecialization("world")


# --- Erasure: runtime type ignores parameters ---------------------------------

def erasure_demo(values: list[int]) -> list[int]:
    # No runtime check that elements are int; erasure means ``list[int]``
    # behaves identically to ``list`` at runtime.
    typed: NewBox[list[int]] = NewBox(values)
    raw: NewBox[list[str]] = typed  # type: ignore[assignment]
    return raw.get()  # type: ignore[return]
