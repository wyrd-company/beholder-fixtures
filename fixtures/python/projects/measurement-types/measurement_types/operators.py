"""Binary, reflected, and in-place operators (PY-CAN-PROT-003)."""

from __future__ import annotations

from typing import Any


class FallbackLeft:
    """Left operand that defers via ``NotImplemented`` for reflected fallback coverage."""

    def __add__(self, other: object) -> Any:
        return NotImplemented


class Reading:
    """Quantity supporting binary, reflected, and in-place operations."""

    def __init__(self, value: float) -> None:
        self.value = value

    def __add__(self, other: object) -> Reading:
        if isinstance(other, Reading):
            return Reading(self.value + other.value)
        if isinstance(other, (int, float)):
            return Reading(self.value + float(other))
        return NotImplemented

    def __radd__(self, other: object) -> Reading:
        if isinstance(other, (int, float)):
            return Reading(float(other) + self.value)
        if isinstance(other, FallbackLeft):
            # Reflected path that accepts the left fallback sentinel so the
            # ``NotImplemented`` demonstration is executable.
            return Reading(self.value + 10)
        return NotImplemented

    def __iadd__(self, other: object) -> Reading:
        if isinstance(other, Reading):
            self.value += other.value
            return self
        if isinstance(other, (int, float)):
            self.value += float(other)
            return self
        return NotImplemented

    def __sub__(self, other: object) -> Reading:
        if isinstance(other, Reading):
            return Reading(self.value - other.value)
        return NotImplemented

    def __rsub__(self, other: object) -> Reading:
        if isinstance(other, (int, float)):
            return Reading(float(other) - self.value)
        return NotImplemented

    def __isub__(self, other: object) -> Reading:
        if isinstance(other, Reading):
            self.value -= other.value
            return self
        return NotImplemented

    def __mul__(self, other: object) -> Reading:
        if isinstance(other, (int, float)):
            return Reading(self.value * float(other))
        return NotImplemented

    def __rmul__(self, other: object) -> Reading:
        return self.__mul__(other)

    def __imul__(self, other: object) -> Reading:
        if isinstance(other, (int, float)):
            self.value *= float(other)
            return self
        return NotImplemented

    def __matmul__(self, other: object) -> Reading:
        if isinstance(other, Reading):
            return Reading(self.value * other.value)
        return NotImplemented

    def __rmatmul__(self, other: object) -> Reading:
        if isinstance(other, Reading):
            return Reading(other.value * self.value)
        return NotImplemented

    def __imatmul__(self, other: object) -> Reading:
        if isinstance(other, Reading):
            self.value *= other.value
            return self
        return NotImplemented

    def __repr__(self) -> str:
        return f"Reading({self.value!r})"


class PriorityReading(Reading):
    """Subtype whose reflected operator is preferred."""

    def __add__(self, other: object) -> Reading:
        if isinstance(other, Reading):
            return PriorityReading(self.value + other.value + 100)
        return NotImplemented

    def __radd__(self, other: object) -> Reading:
        if isinstance(other, Reading):
            return PriorityReading(other.value + self.value + 100)
        return NotImplemented


def subtype_reflection_priority() -> tuple[float, float]:
    """Exercise subtype/reflected priority: subtype wins over base left."""

    base = Reading(10)
    sub = PriorityReading(5)
    left_base = base + sub
    left_sub = sub + base
    return left_base.value, left_sub.value


def fallback_after_notimplemented() -> Reading:
    """Show fallback when left returns ``NotImplemented``."""

    left = FallbackLeft()
    right = Reading(7)
    # ``FallbackLeft.__add__`` returns ``NotImplemented``, so Python tries
    # ``Reading.__radd__`` which handles the sentinel and succeeds.
    result = left + right  # type: ignore[operator]
    assert isinstance(result, Reading)
    return result


def mutation_vs_rebinding() -> tuple[float, float, bool]:
    """Expose mutation versus rebinding through an alias."""

    original = Reading(5)
    alias = original
    # In-place mutates the shared object
    original += Reading(3)
    mutated_value = alias.value
    is_same_after_iadd = alias is original

    detached = Reading(5)
    alias2 = detached
    # Rebinding creates a new object
    detached = detached + Reading(3)
    detached_alias_still_old = alias2.value
    return mutated_value, detached_alias_still_old, is_same_after_iadd


def augmented_attribute_and_item() -> tuple[float, float]:
    """Augmented assignment through attribute and item targets."""

    class Holder:
        def __init__(self) -> None:
            self.value = Reading(10)
            self._data: dict[str, Reading] = {"key": Reading(20)}

        def __getitem__(self, key: str) -> Reading:
            return self._data[key]

        def __setitem__(self, key: str, value: Reading) -> None:
            self._data[key] = value

    holder = Holder()
    holder.value += Reading(5)
    holder["key"] += Reading(5)
    return holder.value.value, holder["key"].value


def later_assignment_failure() -> str:
    """Augmented ``+=`` failure leaves the original binding intact."""

    obj = Reading(4)
    try:
        obj += "bad"  # type: ignore[operator]
        return "no-error"
    except TypeError:
        return f"preserved:{obj.value}"
