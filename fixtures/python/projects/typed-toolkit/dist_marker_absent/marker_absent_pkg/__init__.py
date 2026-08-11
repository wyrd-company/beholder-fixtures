"""Marker-absent package: no py.typed, inline types unadvertised per PEP 561."""

from __future__ import annotations

value: int = 99

def format_value(x: int) -> str:
    return f"unmarked:{x}"
