"""Pure Python accelerator fallback (PY-CAN-INT-008)."""

from __future__ import annotations


def fast_add(a: int, b: int) -> int:
    """Pure Python implementation with parity to native."""
    return a + b


def fast_multiply(a: int, b: int) -> int:
    """Pure multiply fallback."""
    return a * b


ACCEL_IMPL = "pure"
