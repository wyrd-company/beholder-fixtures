"""Partial stub package: py.typed contains 'partial', only some modules stubbed."""

from __future__ import annotations

partial_value: int = 1

def partial_func(x: int) -> str:
    return str(x)

def extra_untyped(x):  # type: ignore[no-untyped-def]
    return x
