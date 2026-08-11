"""Distribution with py.typed marker (PY-CAN-TYPE-016: marker-present)."""

from __future__ import annotations

value: int = 42

def format_value(x: int) -> str:
    return str(x)
