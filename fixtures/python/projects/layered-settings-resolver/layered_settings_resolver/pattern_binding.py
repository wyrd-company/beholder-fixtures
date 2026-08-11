"""Pattern capture scope and irrefutability (PY-CAN-BIND-007)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SettingRecord:
    namespace: str
    key: str
    value: int


def irrefutable_capture(record: SettingRecord) -> tuple[str, str, int]:
    """Bind captures that outlive a successful `match` case."""

    match record:
        case SettingRecord(namespace=scope, key=name, value=amount):
            captured_scope = scope
            captured_name = name
            captured_amount = amount

    return captured_scope, captured_name, captured_amount


def wildcard_no_bind(payload: object) -> str:
    """Show `_` does not create a binding."""

    match payload:
        case [_first, _]:
            label = "pair"
        case _:
            label = "other"

    return label


def qualified_value_pattern(record: SettingRecord) -> str:
    """Match a qualified value pattern against a dataclass instance."""

    match record:
        case SettingRecord(namespace="tenant", key=key, value=value):
            return f"{key}:{value}"
        case SettingRecord(namespace=namespace, key=key, value=_):
            return f"{namespace}/{key}"

    return "unmatched"


def unreachable_or_branch(record: SettingRecord) -> str:
    """Include structurally unequal OR branches that never match."""

    match record:
        case SettingRecord(namespace="tenant", key="mode", value=1) | SettingRecord(
            namespace="tenant",
            key="mode",
            value=2,
        ):
            return "equal-or"
        case SettingRecord(namespace="tenant", key="mode", value=1) | SettingRecord(
            namespace="region",
            key="mode",
            value=1,
        ):
            return "unequal-or-unreachable"

    return "fallback"


def guard_side_effects(record: SettingRecord) -> tuple[bool, int]:
    """Evaluate a guard with observable side effects."""

    counter = 0

    match record:
        case SettingRecord(namespace=namespace, key=key, value=value) if (
            (counter := counter + 1) or True
        ) and namespace == "tenant":
            accepted = True
        case _:
            accepted = False

    return accepted, counter
