"""Cycle participant A — safe late access variant (PY-CAN-MOD-010)."""

from __future__ import annotations

# Import the sibling module object; safe because we only access attributes late.
import content_library.cycles.b as b

value_a = "value-a"

def get_b_value() -> str:
    return b.value_b

# Package-initializer cycle note: if this were imported from ``content_library.cycles.__init__``
# during that package's ``__init__``, the cycle would involve the package initializer.
