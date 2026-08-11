"""Overload sets (PY-CAN-TYPE-009)."""

from __future__ import annotations

from functools import singledispatch
from typing import overload, get_overloads

# --- Overload declarations before one implementation --------------------------

@overload
def process(value: int) -> str: ...

@overload
def process(value: str) -> int: ...

@overload
def process(value: list[int]) -> int: ...

def process(value: int | str | list[int]) -> str | int:
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return len(value)
    return sum(value)


# --- Calls exercising each static shape --------------------------------------

def call_each_shape() -> tuple[str, int, int]:
    a: str = process(42)
    b: int = process("hello")
    c: int = process([1, 2, 3])
    return a, b, c


# --- Runtime get_overloads (Python 3.11+) ------------------------------------

def runtime_overloads_demo() -> tuple[int, str]:
    overloads = get_overloads(process)
    return len(overloads), overloads[0].__name__ if overloads else "none"


# --- Repeated redefinition contrast (not overload) ----------------------------

def redefinition_contrast(x: int) -> int:
    return x * 2


def redefinition_contrast(x: str) -> str:  # noqa: F811 — redefinition replaces prior
    return x.upper()


# --- singledispatch contrast --------------------------------------------------

@singledispatch
def dispatch_process(value: object) -> str:
    return f"generic:{value!r}"


@dispatch_process.register(int)
def _dispatch_int(value: int) -> str:
    return f"int:{value}"


@dispatch_process.register(str)
def _dispatch_str(value: str) -> str:
    return f"str:{value}"


@dispatch_process.register(list)
def _dispatch_list(value: list) -> str:
    return f"list:{len(value)}"


def dispatch_demo() -> tuple[str, str, str]:
    return (
        dispatch_process(42),
        dispatch_process("hello"),
        dispatch_process([1, 2]),
    )


# --- Overlap / unreachable and implementation compatibility note ---------------

# The overload set above has disjoint signatures (int, str, list[int]).
# Overlapping overloads (e.g. ``int`` vs ``object`` ordering) would cause a
# checker to warn about unreachable second overloads.  The implementation
# signature ``int | str | list[int]`` is compatible with all overloads.

@overload
def checked_overload(value: int) -> int: ...

@overload
def checked_overload(value: str) -> str: ...

def checked_overload(value: int | str) -> int | str:
    if isinstance(value, int):
        return value * 2
    return value.upper()
