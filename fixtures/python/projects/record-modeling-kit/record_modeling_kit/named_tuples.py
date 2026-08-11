"""Named tuples (PY-CAN-OBJ-015)."""

from __future__ import annotations

import collections
from typing import Generic, NamedTuple, TypeVar

T = TypeVar("T")

# Factory syntax.
PointTuple = collections.namedtuple("PointTuple", ["x", "y"])


class LabeledPoint(NamedTuple):
    """Class syntax with fields, defaults, annotations, and methods."""

    label: str
    x: int
    y: int = 0

    def distance(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5


class TaggedValue(NamedTuple, Generic[T]):
    """Generic named tuple syntax (Python 3.11+)."""

    tag: str
    value: T


def factory_vs_class_demo() -> tuple[str, str]:
    p1 = PointTuple(1, 2)
    p2 = LabeledPoint("a", 3, 4)
    return type(p1).__name__, type(p2).__name__


def fields_defaults_annotations_demo() -> tuple[str, int, str]:
    lp = LabeledPoint("demo", 5)
    # y defaults to 0
    return lp.label, lp.y, str(LabeledPoint.__annotations__)


def methods_demo() -> float:
    lp = LabeledPoint("m", 3, 4)
    return lp.distance()


def positional_access_demo() -> tuple[int, int]:
    lp = LabeledPoint("p", 10, 20)
    return lp[1], lp[2]


def unpacking_demo() -> tuple[str, int, int]:
    label, x, y = LabeledPoint("u", 1, 2)
    return label, x, y


def immutability_failure_demo() -> str:
    lp = LabeledPoint("imm", 1, 2)
    try:
        lp.x = 99  # type: ignore[misc]
        return "no-error"
    except AttributeError as exc:
        return f"immutable:{exc}"


def invalid_field_rename_demo() -> str:
    # Invalid identifier 'def' is renamed when rename=True.
    Bad = collections.namedtuple("Bad", ["def", "x", "y"], rename=True)
    return str(Bad._fields)


def default_order_demo() -> LabeledPoint:
    # Defaults apply trailing fields; LabeledPoint y defaults.
    return LabeledPoint("order", 7)


def tuple_compatible_equality_demo() -> bool:
    lp = LabeledPoint("t", 1, 2)
    return lp == ("t", 1, 2)


def generic_syntax_demo() -> TaggedValue[int]:
    tv: TaggedValue[int] = TaggedValue("num", 42)
    return tv
