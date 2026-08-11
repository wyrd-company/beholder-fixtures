"""Truth testing and Boolean operands (PY-CAN-PROT-001)."""

from __future__ import annotations


class Quantity:
    """Quantity whose truthiness follows magnitude via ``__bool__``."""

    def __init__(self, amount: float) -> None:
        self.amount = amount

    def __bool__(self) -> bool:
        return self.amount != 0

    def __repr__(self) -> str:
        return f"Quantity({self.amount!r})"


class LengthOnlyContainer:
    """Truthiness via ``__len__`` fallback when ``__bool__`` is absent."""

    def __init__(self, items: list[float]) -> None:
        self._items = list(items)

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"LengthOnlyContainer({self._items!r})"


class BoolDominantContainer:
    """``__bool__`` takes precedence over ``__len__``."""

    def __init__(self, items: list[float]) -> None:
        self._items = list(items)

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        return 0


class BadBoolResult:
    """``__bool__`` returns a non-bool, triggering ``TypeError``."""

    def __bool__(self):  # type: ignore[override]
        return 1  # not a bool


class NegativeLength:
    """``__len__`` returns a negative value, triggering ``ValueError``."""

    def __len__(self) -> int:
        return -1


class AmbiguousMeasure:
    """Truth value that raises, modelling an ambiguous ecosystem object."""

    def __bool__(self) -> bool:
        raise ValueError("ambiguous truth value")


def short_circuit_return(left: object, right_fn: callable) -> object:
    """Show ``and``/``or`` short-circuit return of an operand without evaluating the other."""

    # ``and`` returns left if left is falsy without calling right_fn.
    # ``or`` returns left if left is truthy without calling right_fn.
    # Caller inspects the side-effect counter inside right_fn.
    result_and = left and right_fn()
    result_or = left or right_fn()
    return result_and, result_or


def skipped_side_effect_demo() -> tuple[bool, int]:
    """Demonstrate a skipped right-hand side via ``and``."""

    counter = 0

    def side_effect() -> str:
        nonlocal counter
        counter += 1
        return "evaluated"

    left = Quantity(0)  # falsy
    _ = left and side_effect()
    # counter remains 0 because side_effect was not evaluated
    return bool(left), counter


def not_result(value: object) -> bool:
    """Return ``not`` of a data-model object."""

    return not value
