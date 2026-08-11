"""Stub paired with ``paired_module.py`` drifts on purpose.

Demonstrates stub precedence and drift: runtime defines ``extra_runtime_only``
with ``int`` param, stub declares it with ``str`` param; ``greet`` return type
differs; ``PairedStore`` method signatures diverge.  A checker would surface
these mismatches while runtime remains valid.
"""

value: int

def greet(name: str) -> int: ...
def extra_runtime_only(x: str) -> str: ...
def stub_only_func(x: int) -> str: ...

class PairedStore:
    def get(self, key: str) -> str: ...
    def put(self, key: str, value: str) -> None: ...
