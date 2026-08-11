"""Stub-adjacent runtime module (PY-CAN-TYPE-016 companion).

The distribution artifacts for stub coverage live in subdirectories:
``distribution_with_marker``, ``distribution_without_marker``, ``partial_stub``,
``stub_only``, and ``extension_stub``.  This module holds the runtime Python
implementations that pair with the ``.pyi`` stubs.
"""

from __future__ import annotations


def format_batch(label: str, quantity: int) -> str:
    return f"{label}:{quantity}"


def summarize(values: list[int]) -> int:
    return sum(values)


class BatchStore:
    def __init__(self) -> None:
        self._data: dict[str, int] = {}

    def add(self, label: str, quantity: int) -> None:
        self._data[label] = quantity

    def get(self, label: str) -> int | None:
        return self._data.get(label)
