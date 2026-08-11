"""Private implementation for re-export facade (PY-CAN-MOD-009)."""

from __future__ import annotations

_internal_token = "private-impl-token"


class InternalWidget:
    """Implementation type re-exported through the facade."""

    def __init__(self, label: str) -> None:
        self.label = label

    def render(self) -> str:
        return f"widget:{self.label}"


# Private helper not intended for public use.
def _private_helper(value: str) -> str:
    return f"helper:{value}"


PUBLIC_CONSTANT = "public-via-impl"
