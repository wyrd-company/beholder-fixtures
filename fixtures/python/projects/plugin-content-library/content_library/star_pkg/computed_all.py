"""Computed ``__all__`` surface (PY-CAN-MOD-008)."""

alpha = "alpha"
beta = "beta"
gamma = "gamma"
_internal = "hidden"

_candidates = ["alpha", "beta", "gamma"]
__all__ = [name for name in _candidates if not name.startswith("_")]
