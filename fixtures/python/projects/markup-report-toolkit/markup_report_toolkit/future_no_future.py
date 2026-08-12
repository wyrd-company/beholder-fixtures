"""Helper without future import (PY-CAN-SRC-003 imported non-inheritance)."""

class NoFutureNode:
    """Annotations evaluated without postponed flag; forward ref would be string only with future."""

    value: int
    next: "NoFutureNode | None"
