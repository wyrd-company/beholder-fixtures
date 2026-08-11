"""Pattern capture scope and irrefutability (PY-CAN-BIND-007)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass
class SettingRecord:
    namespace: str
    key: str
    value: int


class Namespace(Enum):
    TENANT = "tenant"
    REGION = "region"


class SettingsNamespace:
    TENANT = "tenant"


def irrefutable_capture(record: SettingRecord) -> tuple[str, str, int]:
    """Bind captures that outlive a successful `match` case."""

    match (record.namespace, record.key, record.value):
        case (scope, name, amount):
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
        case SettingRecord(namespace=SettingsNamespace.TENANT, key=key, value=value):
            return f"{key}:{value}"
        case SettingRecord(namespace=namespace, key=key, value=_):
            return f"{namespace}/{key}"

    return "unmatched"


def failed_match_partial_binding(payload: object) -> tuple[bool, str | None]:
    """Capture a name before a later component of the same pattern fails.

    The sequence subpattern binds ``head`` from element zero, then the trailing
    literal is compared. A payload whose second element is not ``"sentinel"``
    partially matches: ``head`` is captured and the case then fails. Whether
    CPython leaves ``head`` bound after that failed match is unspecified, so the
    failure path never reads it.
    """

    matched = False
    selected: str | None = None

    match payload:
        case [head, "sentinel"]:
            matched = True
            selected = head
        case _:
            pass

    return matched, selected


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
