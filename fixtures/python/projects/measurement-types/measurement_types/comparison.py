"""Rich comparison and chaining (PY-CAN-PROT-002)."""

from __future__ import annotations

import functools


class Measure:
    """Base quantity with rich comparisons."""

    def __init__(self, value: float) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Measure):
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Measure):
            return self.value < other.value
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, Measure):
            return self.value <= other.value
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Measure):
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Measure):
            return self.value >= other.value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return f"Measure({self.value!r})"


class SpecialMeasure(Measure):
    """Subclass whose ``__eq__`` is preferred via subclass priority."""

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Measure):
            # Distinguish subclass dispatch by negating value check on equal magnitude
            if self.value == other.value:
                return False
            return self.value == other.value
        return NotImplemented


class ReflectedOnly:
    """Type that only implements reflected comparison."""

    def __init__(self, value: float) -> None:
        self.value = value

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Measure):
            return self.value > other.value
        return NotImplemented

    def __repr__(self) -> str:
        return f"ReflectedOnly({self.value!r})"


@functools.total_ordering
class OrderedReading:
    """Derive total ordering from ``__eq__`` and ``__lt__``."""

    def __init__(self, value: float) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, OrderedReading):
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, OrderedReading):
            return self.value < other.value
        return NotImplemented

    def __repr__(self) -> str:
        return f"OrderedReading({self.value!r})"


class OrderingFailure:
    """Returns ``NotImplemented`` for ordering, producing ``TypeError``."""

    def __lt__(self, other: object) -> bool:
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        return NotImplemented


def chained_evaluation_demo() -> tuple[bool, int]:
    """Show that ``a < b < c`` evaluates middle operand once."""

    counter = {"calls": 0}

    class CountingMeasure(Measure):
        def __lt__(self, other: object) -> bool:
            counter["calls"] += 1
            return super().__lt__(other)

    a = CountingMeasure(1)
    b = CountingMeasure(2)
    c = CountingMeasure(3)
    result = a < b < c
    return result, counter["calls"]


def notimplemented_versus_raise() -> tuple[str, str]:
    """Contrast ``NotImplemented`` fallback with a raising comparator."""

    class RaisingMeasure(Measure):
        def __eq__(self, other: object) -> bool:
            raise RuntimeError("comparison error")

    base = Measure(5)
    # NotImplemented path: base compared to incompatible type falls back to identity
    notimpl_result = "equal" if base == object() else "not-equal"
    raising = RaisingMeasure(5)
    try:
        _ = raising == Measure(5)
        raising_result = "no-error"
    except RuntimeError:
        raising_result = "runtime-error"
    return notimpl_result, raising_result


def identity_fallback_for_equality() -> bool:
    """Show identity fallback when both sides return ``NotImplemented``."""

    class Left:
        def __eq__(self, other: object) -> bool:
            return NotImplemented

    class Right:
        def __eq__(self, other: object) -> bool:
            return NotImplemented

    left = Left()
    right = Right()
    # left == right falls back to identity (left is right)
    return (left == right) is (left is right)
