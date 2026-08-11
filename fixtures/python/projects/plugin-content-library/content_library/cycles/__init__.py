"""Cycle package init (PY-CAN-MOD-010) — demonstrates package-initializer cycle."""

from . import a as _a

__all__ = ["_a"]
