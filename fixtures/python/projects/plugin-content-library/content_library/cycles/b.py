"""Cycle participant B — counterpart to A (PY-CAN-MOD-010)."""

from __future__ import annotations

import content_library.cycles.a as a

value_b = "value-b"

def get_a_value() -> str:
    return a.value_a

# Failing early ``from`` access variant would be:
# from content_library.cycles.a import value_a  # fails during cycle if a not yet defining value_a
# That shape is demonstrated in ``failure_demo.py`` via a controlled two-module cycle.
