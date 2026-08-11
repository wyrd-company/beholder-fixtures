"""Call unpacking and evaluation order (PY-CAN-CALL-003)."""

from __future__ import annotations

from collections.abc import Iterable


def record_call(a: str, b: str, c: str, *, tag: str = "default", **extras: str) -> dict[str, object]:
    """Target whose call site exercises unpacking."""

    return {"a": a, "b": b, "c": c, "tag": tag, "extras": dict(extras)}


def interleaved_unpacking_with_side_effects() -> tuple[dict[str, object], list[str]]:
    """Interleave iterable and mapping unpackings with observable side effects."""

    log: list[str] = []

    def left_items() -> Iterable[str]:
        log.append("left")
        yield "alpha"
        yield "beta"

    def right_items() -> Iterable[str]:
        log.append("right")
        yield "gamma"

    def mapping_items() -> dict[str, str]:
        log.append("mapping")
        return {"tag": "express", "channel": "parcel"}

    result = record_call(*left_items(), *right_items(), **mapping_items())
    return result, log


def left_to_right_evaluation() -> list[str]:
    """Unpacking arguments are evaluated strictly left-to-right."""

    order: list[str] = []

    def step(name: str, value: list[str]) -> list[str]:
        order.append(name)
        return value

    def mapping_step(name: str, value: dict[str, str]) -> dict[str, str]:
        order.append(name)
        return value

    record_call(
        *step("first", ["a"]),
        *step("second", ["b"]),
        "c",
        **mapping_step("third", {"tag": "bulk"}),
        **mapping_step("fourth", {"extra": "x"}),
    )
    return order


def duplicate_keyword_failure() -> str:
    """Duplicate keyword via ``**`` unpacking must raise ``TypeError``."""

    try:
        record_call("a", "b", "c", **{"tag": "one"}, **{"tag": "two"})  # type: ignore[arg-type]
        return "no-error"
    except TypeError:
        return "type-error"


def non_string_keyword_failure() -> str:
    """Non-string mapping keys via ``**`` must raise ``TypeError``."""

    try:
        record_call("a", "b", "c", **{1: "numeric"})  # type: ignore[arg-type]
        return "no-error"
    except TypeError:
        return "type-error"


class CustomMapping:
    """Custom mapping whose iteration yields string keys."""

    def __init__(self, data: dict[str, str]) -> None:
        self._data = data

    def keys(self):
        return self._data.keys()

    def __getitem__(self, key: str) -> str:
        return self._data[key]


def custom_mapping_unpacking() -> dict[str, object]:
    """Unpack a custom mapping type via ``**``."""

    custom = CustomMapping({"tag": "custom", "extra": "value"})
    return record_call("a", "b", "c", **custom)  # type: ignore[arg-type]


def custom_mapping_iteration() -> list[str]:
    """Iterate a custom mapping to show custom ``keys`` protocol."""

    custom = CustomMapping({"x": "1", "y": "2"})
    return list(custom.keys())
