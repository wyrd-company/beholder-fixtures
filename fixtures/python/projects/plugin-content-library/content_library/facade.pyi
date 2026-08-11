"""Stub demonstrating drift from runtime (PY-CAN-MOD-009).

Runtime ``facade.Widget`` lacks ``extra_stub_only``; stub claims it exists.
"""

from pathlib import Path as ContentPath

class Widget:
    label: str
    def __init__(self, label: str) -> None: ...
    def render(self) -> str: ...
    def extra_stub_only(self) -> str: ...  # drift: not present at runtime

PUBLIC_CONSTANT: str
