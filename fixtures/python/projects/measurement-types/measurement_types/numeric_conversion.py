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


def conversion_fallback_demo() -> tuple[int, float]:
    """Contrast ``int(obj)`` (``__int__``) with ``obj.__index__()``."""

    obj = IndexLike(index_value=3, int_value=9)
    return int(obj), obj.__index__()


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
