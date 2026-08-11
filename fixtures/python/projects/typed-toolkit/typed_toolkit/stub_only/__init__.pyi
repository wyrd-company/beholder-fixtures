"""Stub-only package (PY-CAN-TYPE-016: stub-only).

This artifact provides only a ``.pyi`` file without a corresponding ``.py``;
it represents a stub-only distribution as used for external typed stubs.
"""

from typing import TypedDict

class StubOnlyRecord(TypedDict):
    label: str
    quantity: int

def fetch_record(label: str) -> StubOnlyRecord: ...

value: int = ...
