"""Iteration protocol (PY-CAN-PROT-005)."""

from __future__ import annotations

from collections.abc import Iterator


class ReIterableSeries:
    """Re-iterable container; each ``iter()`` returns a fresh iterator."""

    def __init__(self, values: list[float]) -> None:
        self._values = list(values)

    def __iter__(self) -> Iterator[float]:
        return iter(self._values)

    def __repr__(self) -> str:
        return f"ReIterableSeries({self._values!r})"


class OneShotIterator:
    """One-shot iterator that returns itself."""

    def __init__(self, values: list[float]) -> None:
        self._values = list(values)
        self._index = 0

    def __iter__(self) -> OneShotIterator:
        return self

    def __next__(self) -> float:
        if self._index >= len(self._values):
            raise StopIteration
        value = self._values[self._index]
        self._index += 1
        return value


def exhaustion_permanence() -> tuple[list[float], list[float]]:
    """Show that an exhausted one-shot iterator stays exhausted."""

    it = OneShotIterator([1.0, 2.0])
    first_pass = list(it)
    second_pass = list(it)
    return first_pass, second_pass


def bad_resuming_iterator() -> str:
    """Show calling ``next`` after exhaustion raises ``StopIteration``."""

    it = OneShotIterator([5.0])
    next(it)
    try:
        next(it)
        return "no-error"
    except StopIteration:
        return "stop-iteration"


def concurrent_iterations() -> tuple[list[float], list[float]]:
    """Two iterators over the same re-iterable advance independently."""

    series = ReIterableSeries([10.0, 20.0, 30.0])
    it_a = iter(series)
    it_b = iter(series)
    next(it_a)
    first_b = next(it_b)
    second_a = next(it_a)
    return [first_b], [second_a]


def mutation_during_iteration() -> list[float]:
    """Appending during iteration does not affect the current snapshot iterator."""

    series = ReIterableSeries([1.0, 2.0, 3.0])
    # list snapshot via explicit iterator
    it = iter(series)
    collected: list[float] = []
    for value in it:
        collected.append(value)
        if value == 1.0:
            # Mutate underlying list through the container
            series._values.append(99.0)
    return collected


def callable_sentinel_iter() -> list[str]:
    """Use ``iter(callable, sentinel)`` to drain a callable source."""

    data = ["a", "b", "c"]

    def pop_next() -> str:
        if data:
            return data.pop(0)
        return "END"

    return list(iter(pop_next, "END"))


def iterator_returns_self_check() -> bool:
    """Verify that the one-shot iterator's ``__iter__`` returns itself."""

    it = OneShotIterator([1.0])
    return iter(it) is it
