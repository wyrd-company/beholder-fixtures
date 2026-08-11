"""Partial stub package (PY-CAN-TYPE-016: partial).

The ``py.typed`` marker contains ``partial`` indicating that only some modules
have stubs; missing stubs are treated as untyped.
"""

from __future__ import annotations

partial_value: int = 1

def partial_func(x: int) -> str:
    return str(x)

# ``extra_untyped`` has no stub entry; it remains untyped in partial mode.
def extra_untyped(x):  # type: ignore[no-untyped-def]
    return x
