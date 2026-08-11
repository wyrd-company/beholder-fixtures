"""Distribution without py.typed marker (PY-CAN-TYPE-016: marker-absent).

Inline types are present but the distribution is unmarked, so a checker may
ignore inline annotations per PEP 561.
"""

from __future__ import annotations

value: int = 99

def format_value(x: int) -> str:
    return f"unmarked:{x}"
