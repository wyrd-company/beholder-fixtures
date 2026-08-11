"""Pattern-matching protocols (PY-CAN-PROT-011).

Note: mapping/sequence protocol call counts during pattern matching
(e.g., ``__getitem__``, ``__iter__``, ``get``) are partly unspecified per
PEP 634; a valid source must not assert a fixed number of protocol calls.
"""

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


class DuplicateKeys:
    """Qualified keys that resolve to the same mapping key value."""

    K1 = "dup"
    K2 = "dup"


def duplicate_mapping_key_demo() -> str:
    """Exercise duplicate mapping keys via qualified constants.

    Two qualified keys ``DuplicateKeys.K1`` and ``DuplicateKeys.K2`` both
    resolve to ``"dup"``. Literal duplicate ``{"dup": a, "dup": b}``
    is rejected at compile time (SyntaxError); the qualified form is
    valid source that exercises the runtime duplicate-key handling which
    raises ``ValueError`` when evaluated.
    """

    payload = {"dup": 7, "other": 1}
    try:
        match payload:
            case {DuplicateKeys.K1: a, DuplicateKeys.K2: b}:
                return f"matched:{a},{b}"
            case _:
                return "no-match"
    except ValueError as exc:
        return f"value-error:{exc}"
