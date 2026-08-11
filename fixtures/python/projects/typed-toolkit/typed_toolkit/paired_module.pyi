"""Stub paired with ``paired_module.py``.

Demonstrates stub precedence and drift potential: stub and runtime must stay
aligned or drift occurs.
"""

value: int

def greet(name: str) -> str: ...

class PairedStore:
    def get(self, key: str) -> int | None: ...
    def put(self, key: str, value: int) -> None: ...
