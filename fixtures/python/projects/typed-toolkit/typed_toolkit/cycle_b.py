"""Cycle participant B (PY-CAN-TYPE-021)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typed_toolkit.cycle_a import Batch


class Record:
    def __init__(self, value: int) -> None:
        self.value = value

    def describe(self, batch: "Batch") -> str:  # type: ignore[valid-type]
        return f"record:{self.value} batch:{batch.label}"


def make_record(value: int, batch: "Batch | None" = None) -> Record:  # type: ignore[valid-type]
    r = Record(value)
    if batch is not None:
        _ = r.describe(batch)
    return r
