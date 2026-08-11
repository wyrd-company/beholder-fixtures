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
    """Measure exposing only ``__trunc__``.

    ``math.trunc`` calls ``__trunc__`` directly; that is the supported
    truncation protocol. ``int()`` no longer falls back to ``__trunc__``: the
    delegation of ``int()`` to ``__trunc__`` was deprecated in Python 3.11 and
    removed in 3.14, so ``int()`` on a ``__trunc__``-only object raises
    ``TypeError``. Neither ``__int__`` nor ``__index__`` is defined here, so no
    other conversion protocol can mask that removal.
    """

    def __init__(self, value: float) -> None:
        self.value = value

    def __trunc__(self) -> int:
        return int(self.value)


def conversion_fallback_demo() -> tuple[int, int, int]:
    """Contrast ``int()`` conversion fallback with the direct index protocol.

    ``IndexOnlyFallback`` implements only ``__index__``. Because it has no
    ``__int__``, ``int()`` falls back to ``__index__`` -- this is the conversion
    fallback. ``operator.index`` is not a fallback: it invokes ``__index__``
    directly and unconditionally, so it serves as the exact-index contrast. An
    explicit ``IndexLike.__index__()`` call is a third, direct form.
    """

    import operator

    fallback_obj = IndexOnlyFallback()
    # ``int`` has no ``__int__`` to call, so it falls back to ``__index__``.
    fallback_via_int = int(fallback_obj)
    # ``operator.index`` always calls ``__index__`` directly -- not a fallback.
    direct_via_index = operator.index(fallback_obj)
    # Explicit dunder call on an object that defines both conversions.
    direct_explicit = IndexLike(index_value=3, int_value=9).__index__()
    return fallback_via_int, direct_via_index, direct_explicit


def deprecated_truncation_demo() -> tuple[int, str]:
    """Contrast supported ``math.trunc`` with the removed ``int`` -> ``__trunc__`` fallback.

    ``math.trunc`` invokes ``__trunc__`` directly and remains supported.
    Historically ``int()`` fell back to ``__trunc__`` when ``__int__`` and
    ``__index__`` were absent; that delegation was deprecated in Python 3.11 and
    removed in 3.14. On 3.14 ``int()`` of a ``__trunc__``-only object therefore
    raises ``TypeError`` -- there is no ``operator.trunc`` counterpart, and
    ``math.trunc`` is the only remaining direct route to ``__trunc__``.
    """

    import math

    obj = TruncatableMeasure(3.7)
    supported = math.trunc(obj)  # -> 3, via __trunc__
    try:
        removed_fallback: str = str(int(obj))
    except TypeError:
        removed_fallback = "type-error"
    return supported, removed_fallback


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
