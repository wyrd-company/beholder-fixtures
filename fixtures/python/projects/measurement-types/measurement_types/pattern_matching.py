"""Pattern-matching protocols (PY-CAN-PROT-011)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


class BoundedMeasure:
    __match_args__ = ("value", "unit")

    def __init__(self, value: float, unit: str) -> None:
        self.value = value
        self.unit = unit


class Units:
    KG = "kg"
    M = "m"


UNIT_KG = Units.KG
UNIT_M = Units.M


def match_sequence(payload: object) -> str:
    """Match sequence patterns, excluding strings as sequences."""

    match payload:
        case [first, second]:
            return f"pair:{first},{second}"
        case [first, *rest]:
            return f"head:{first},rest:{len(rest)}"
        case _:
            return "no-sequence"


def match_mapping(payload: object) -> str:
    """Match mapping patterns with duplicate-key and ``get`` semantics."""

    match payload:
        case {"kind": "length", "value": v}:
            return f"length:{v}"
        case {"kind": kind, "value": v}:
            return f"{kind}:{v}"
        case _:
            return "no-mapping"


def match_class(payload: object) -> str:
    """Match class patterns with ``__match_args__`` and keyword forms."""

    match payload:
        case Point(x, y) if x == y:
            return f"diagonal:{x}"
        case Point(x=x, y=y):
            return f"point:{x},{y}"
        case BoundedMeasure(value, unit):
            return f"bounded:{value}{unit}"
        case _:
            return "no-class"


def match_literal_and_or(payload: object) -> str:
    """Match literal, OR, AS, and wildcard patterns with guards."""

    match payload:
        case 0 | 0.0:
            return "zero"
        case "kg" | "m":
            return "unit-literal"
        case value as named if isinstance(named, int) and named > 10:
            return f"large:{value}"
        case _:
            return "wildcard"


def match_nested_and_guard(payload: object) -> str:
    """Nested patterns and guarded cases."""

    match payload:
        case {"reading": Point(x, y) as pt} if x > 0:
            return f"nested:{pt.x},{pt.y}"
        case [Point(x, y), {"value": v}]:
            return f"nested-seq:{x},{y}:{v}"
        case _:
            return "no-nested"


def qualified_constant_match(payload: object) -> str:
    """Match qualified constant value patterns."""

    match payload:
        case Units.KG:
            return "kg-const"
        case Units.M:
            return "m-const"
        case _:
            return "other-const"


def string_excluded_as_sequence(payload: object) -> str:
    """Show that strings are not matched as sequences."""

    match payload:
        case [first, *_]:
            return f"seq:{first}"
        case str() as text:
            return f"str:{text}"
        case _:
            return "other"


def duplicate_mapping_key_demo() -> str:
    """Exercise mapping pattern where duplicate key handling is defined by syntax.

    Python grammar rejects a literal duplicate mapping key in a single pattern.
    The closest runtime variant is two overlapping keys across an OR.
    """

    payload = {"value": 7, "value2": 7}  # not duplicate; pattern uses one key

    match payload:
        case {"value": a} | {"value": a}:  # OR of same key
            return f"or-value:{a}"
        case _:
            return "no-or"
