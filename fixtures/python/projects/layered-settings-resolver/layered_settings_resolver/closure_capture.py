"""Closures and late binding (PY-CAN-BIND-003)."""

from __future__ import annotations

from types import CellType


def loop_late_binding(keys: list[str]) -> list[callable]:
    """Create loop closures that share one late-bound cell per iteration."""

    resolvers: list[callable] = []
    for key in keys:
        resolvers.append(lambda current=key: current.upper())
    return resolvers


def factory_capture(default: str) -> tuple[callable, callable]:
    """Contrast default-argument capture with per-call factory binding."""

    def default_bound(value: str = default) -> str:
        return value

    def factory_bound() -> str:
        return default

    return default_bound, factory_bound


def nonlocal_cell_mutation() -> int:
    """Mutate a captured cell through `nonlocal`."""

    total = 0

    def add(amount: int) -> None:
        nonlocal total
        total += amount

    add(3)
    add(5)
    return total


def deleted_free_variable() -> str | None:
    """Remove a free variable after creating a closure that captured it."""

    token = "layer-token"

    def reader() -> str:
        return token

    snapshot = reader
    del token
    return snapshot()


def one_closure_per_factory_call() -> tuple[callable, callable]:
    """Return distinct closure objects from repeated factory calls."""

    def make_reader(label: str):
        captured = label

        def reader() -> str:
            return captured

        return reader

    first = make_reader("alpha")
    second = make_reader("beta")
    return first, second


def qualified_locals_name() -> str:
    """Surface a nested function's qualified `<locals>` name."""

    def outer():
        def inner() -> str:
            return inner.__qualname__

        return inner

    nested = outer()
    return nested()


def closure_cell_type(reader: callable) -> bool:
    """Inspect closure cells for a nested callable."""

    closure = reader.__closure__
    if closure is None:
        return False
    return all(isinstance(cell, CellType) for cell in closure)
