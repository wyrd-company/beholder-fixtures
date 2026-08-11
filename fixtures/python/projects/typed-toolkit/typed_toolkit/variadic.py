"""Variadic generics (PY-CAN-TYPE-014)."""

from __future__ import annotations

from typing import Callable, Generic, TypeVar, TypeVarTuple, Unpack

T = TypeVar("T")
Ts = TypeVarTuple("Ts")
Ts2 = TypeVarTuple("Ts2")

# --- Basic TypeVarTuple API --------------------------------------------------

class VariadicBox(Generic[Unpack[Ts]]):
    def __init__(self, *values: Unpack[Ts]) -> None:
        self.values: tuple[Unpack[Ts]] = values

    def as_tuple(self) -> tuple[Unpack[Ts]]:
        return self.values


# --- Specialize with zero, one, and many elements ----------------------------

EmptyBox: type[VariadicBox[()]] = VariadicBox
SingleBox: type[VariadicBox[int]] = VariadicBox
ManyBox: type[VariadicBox[int, str, float]] = VariadicBox


def specialize_zero() -> VariadicBox[()]:
    return VariadicBox()

def specialize_one() -> VariadicBox[int]:
    return VariadicBox(42)

def specialize_many() -> VariadicBox[int, str, float]:
    return VariadicBox(1, "hello", 3.14)


# --- One variadic tuple per parameter list -----------------------------------

# Only one TypeVarTuple is permitted per parameter list (PEP 646).  A second
# variadic pack would be ``Generic[Unpack[Ts], Unpack[Ts2]]`` and fails at
# runtime, so it is shown as a commented invalid variant.  The valid unpack
# spelling uses a single ``Unpack`` per prefix/suffix.
# class TwoPacks(Generic[Unpack[Ts], Unpack[Ts2]]): ...  # invalid: two packs
class SinglePack(Generic[Unpack[Ts]]):
    pass


# --- Unpack spelling variants -------------------------------------------------

def accepts_variadic(*args: Unpack[Ts]) -> tuple[Unpack[Ts]]:
    return args


def forwards_variadic(
    func: Callable[[Unpack[Ts]], T],
    *args: Unpack[Ts],
) -> T:
    return func(*args)


def tuple_unpack_demo(values: tuple[int, str]) -> tuple[int, str]:
    # Unpacking a variadic tuple into a callable
    def pair(a: int, b: str) -> tuple[int, str]:
        return a, b

    return forwards_variadic(pair, *values)  # type: ignore[arg-type]


# --- Mixing ordinary variables and defaults -----------------------------------

U = TypeVar("U")

class MixedVariadic(Generic[T, Unpack[Ts], U]):
    def __init__(self, first: T, *rest: Unpack[Ts], last: U) -> None:
        self.first = first
        self.rest = rest
        self.last = last


def mixed_demo() -> MixedVariadic[int, str, float, bool]:
    # T=int, Ts=(str, float), U=bool
    return MixedVariadic(1, "a", 3.14, last=True)


# Variadic with ordinary type vars and default-ish usage
def variadic_with_defaults[T, *Ts](first: T, *rest: Unpack[Ts]) -> tuple[T, tuple[Unpack[Ts]]]:
    return first, rest


# --- Callable with variadic generics -----------------------------------------

def apply_variadic(func: Callable[[Unpack[Ts]], T], *args: Unpack[Ts]) -> T:
    return func(*args)
