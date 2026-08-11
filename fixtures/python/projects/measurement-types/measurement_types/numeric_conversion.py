"""Numeric conversion and exact-index protocol (PY-CAN-PROT-009)."""

from __future__ import annotations


class IndexLike:
    """Object with distinct ``__index__`` and ``__int__`` values."""

    def __init__(self, index_value: int, int_value: int) -> None:
        self._index = index_value
        self._int = int_value

    def __index__(self) -> int:
        return self._index

    def __int__(self) -> int:
        return self._int

    def __float__(self) -> float:
        return float(self._int)

    def __complex__(self) -> complex:
        return complex(self._int)

    def __repr__(self) -> str:
        return f"IndexLike(index={self._index}, int={self._int})"


class StrictIndex:
    """``__index__`` that violates strict ``int`` return type."""

    def __index__(self):  # type: ignore[override]
        return "bad"  # type: ignore[return-value]


class BoolSubtypeDemo:
    """Show ``bool`` as a subtype of ``int`` with distinct protocol behavior."""

    @staticmethod
    def bool_is_int_subtype() -> bool:
        return issubclass(bool, int)

    @staticmethod
    def bool_index_usage(values: list[str]) -> str:
        # ``True`` indexes as 1, ``False`` as 0
        return values[True]


def range_with_index_demo() -> list[int]:
    """Use ``__index__`` in ``range`` construction."""

    stop = IndexLike(5, 99)
    return list(range(stop))


def slice_with_index_demo(values: list[int]) -> list[int]:
    """Use ``__index__`` for slice bounds."""

    start = IndexLike(1, 99)
    stop = IndexLike(4, 99)
    return values[start:stop]


def bytes_with_index_demo() -> bytes:
    """Use ``__index__`` for a ``bytes`` length."""

    length = IndexLike(4, 99)
    return bytes(length)


class IndexOnlyFallback:
    """Object with ``__index__`` only; ``int()`` falls back to it."""

    def __index__(self) -> int:
        return 7


class TruncatableMeasure:
    """Measure exposing the deprecated truncation path via ``__trunc__``."""

    def __init__(self, value: float) -> None:
        self.value = value

    def __int__(self) -> int:
        return int(self.value)

    def __index__(self) -> int:
        return int(self.value) + 10

    def __trunc__(self) -> int:
        return int(self.value) + 100


def conversion_fallback_demo() -> tuple[int, int, int]:
    """Exercise conversion fallback from ``__int__`` to ``__index__``.

    ``IndexOnlyFallback`` implements only ``__index__``. ``int()`` and
    ``operator.index`` fall back to ``__index__`` when ``__int__`` is absent,
    distinct from the direct ``obj.__index__()`` call on ``IndexLike`` which
    implements both and would otherwise be confused with fallback.
    """

    import operator

    fallback_obj = IndexOnlyFallback()
    # ``int`` falls back to ``__index__`` when ``__int__`` is missing.
    fallback_via_int = int(fallback_obj)  # uses __index__
    fallback_via_index = operator.index(fallback_obj)
    direct = IndexLike(index_value=3, int_value=9).__index__()
    return fallback_via_int, fallback_via_index, direct


def deprecated_truncation_demo() -> tuple[int, int, int]:
    """Demonstrate the deprecated truncation path ``__trunc__``.

    ``math.trunc`` and ``operator.trunc`` prefer ``__trunc__`` over
    ``__int__``/``__index__``, representing the historical truncation
    route. ``TruncatableMeasure`` exposes all three for comparison.
    """

    import math
    import operator

    obj = TruncatableMeasure(3.7)
    return math.trunc(obj), operator.index(obj), int(obj)


def strict_return_type_demo() -> str:
    """Show strict return type check for ``__index__``."""

    bad = StrictIndex()
    try:
        _ = [1, 2, 3][bad]  # type: ignore[index]
        return "no-error"
    except TypeError:
        return "type-error"


def bool_subtype_demo() -> tuple[bool, str]:
    """Show ``bool`` index versus ``int`` conversion distinction."""

    return BoolSubtypeDemo.bool_is_int_subtype(), BoolSubtypeDemo.bool_index_usage(["zero", "one", "two"])


def operator_index_demo() -> int:
    """Use ``__index__`` through the ``operator.index`` helper."""

    import operator

    obj = IndexLike(7, 3)
    return operator.index(obj)
