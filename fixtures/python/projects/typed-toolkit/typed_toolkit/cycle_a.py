"""Cycle participant A (PY-CAN-TYPE-021)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typed_toolkit.cycle_b import Record


class Batch:
    def __init__(self, label: str) -> None:
        self.label = label

    def related(self, record: "Record") -> str:  # type: ignore[valid-type]
        return f"{self.label}:{record.value}"


def make_batch(label: str, record: "Record | None" = None) -> Batch:  # type: ignore[valid-type]
    b = Batch(label)
    if record is not None:
        _ = b.related(record)
    return b
