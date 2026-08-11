"""`global` and `nonlocal` declarations (PY-CAN-BIND-002)."""

from __future__ import annotations

_shared_counter: dict[str, int] = {"value": 0}


def rebind_module_global(increment: int) -> int:
    """Rebind a module-level name through `global`."""

    global _shared_counter
    _shared_counter = {"value": _shared_counter["value"] + increment}
    return _shared_counter["value"]


def rebind_enclosing() -> tuple[int, int]:
    """Rebind an enclosing function name through `nonlocal`."""

    tally = 1

    def outer() -> int:
        nonlocal tally
        tally += 1
        return tally

    def inner() -> int:
        nonlocal tally
        tally += 10
        return tally

    first = outer()
    second = inner()
    return first, second


def mutate_without_declaration() -> list[str]:
    """Mutate a shared object without `global` or `nonlocal`."""

    layers: list[str] = ["base"]

    def append_layer(name: str) -> None:
        layers.append(name)

    append_layer("region")
    append_layer("tenant")
    return layers


def parameter_shadows_enclosing() -> str:
    """Show a parameter name shadows an enclosing binding without `nonlocal`."""

    label = "enclosing"

    def worker(label: str) -> str:
        return label

    return worker("parameter-wins")


def missing_nonlocal_reads_enclosing() -> int:
    """Read an enclosing name without rebinding it."""

    seed = 4

    def reader() -> int:
        return seed + 1

    return reader()
