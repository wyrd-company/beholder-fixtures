"""Explicit ``__all__`` surface (PY-CAN-MOD-008)."""

public_a = "a"
public_b = "b"
_private = "should-not-export-via-star"

__all__ = ["public_a", "public_b"]
