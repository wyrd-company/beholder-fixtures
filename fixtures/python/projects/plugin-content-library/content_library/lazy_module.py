"""Module-level dynamic attributes (PY-CAN-MOD-014).

Implements :pep:`562` ``__getattr__`` / ``__dir__`` at module scope.

Variants:

- internal global lookup bypass (``__getattr__`` not consulted for existing globals)
- missing name must raise ``AttributeError``
- deprecation alias
- ``__all__`` and stub mismatch
"""

from __future__ import annotations

import warnings

# Existing global — __getattr__ is not consulted for this name.
existing_global = "present-global"

# Internal deprecation mapping.
_deprecated = {"old_name": "lazy_value"}

__all__ = ["existing_global", "lazy_value", "old_name"]


def __getattr__(name: str) -> object:
    if name == "lazy_value":
        return "computed-lazy-value"
    if name in _deprecated:
        warnings.warn(f"{name} is deprecated, use {_deprecated[name]}", DeprecationWarning, stacklevel=2)
        return "computed-lazy-value"
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    # Custom dir includes lazy and deprecated names plus existing globals.
    return sorted(["existing_global", "lazy_value", "old_name", "__all__"])


# Drift note: ``lazy_module.pyi`` stub lists an extra name ``stub_only``.
