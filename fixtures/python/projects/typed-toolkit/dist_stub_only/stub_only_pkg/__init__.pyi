"""Stub-only package: only .pyi, no .py, representing stub-only distribution."""

from typing import TypedDict

class StubOnlyRecord(TypedDict):
    label: str
    quantity: int

def fetch_record(label: str) -> StubOnlyRecord: ...

value: int = ...
