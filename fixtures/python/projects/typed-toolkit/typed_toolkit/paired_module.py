"""Paired .py with .pyi example (PY-CAN-TYPE-016: stub)."""

from __future__ import annotations

value: int = 7

def greet(name: str) -> str:
    return f"hello {name}"

def extra_runtime_only(x: int) -> int:
    return x * 2

class PairedStore:
    def get(self, key: str) -> int | None:
        return None

    def put(self, key: str, value: int) -> None:
        pass
