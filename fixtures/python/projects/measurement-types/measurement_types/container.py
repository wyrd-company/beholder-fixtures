"""Container protocols (PY-CAN-PROT-004)."""

from __future__ import annotations

from collections.abc import Iterator


class IndexValue:
    """Object with ``__index__`` distinct from ``__int__``."""

    def __init__(self, index: int, numeric: int) -> None:
        self._index = index
        self._numeric = numeric

    def __index__(self) -> int:
        return self._index

    def __int__(self) -> int:
        return self._numeric

    def __repr__(self) -> str:
        return f"IndexValue(index={self._index}, int={self._numeric})"


class MeasurementSeries:
    """Sequence-like container with length, indexing, slicing, and membership."""

    def __init__(self, values: list[float]) -> None:
        self._values = list(values)

    def __len__(self) -> int:
        return len(self._values)

    def __getitem__(self, key: int | slice) -> float | list[float]:
        if isinstance(key, slice):
            return self._values[key]
        # Negative indexes delegated to the underlying list
        return self._values[key]

    def __setitem__(self, key: int | slice, value: float | list[float]) -> None:
        if isinstance(key, slice):
            assert isinstance(value, list)
            self._values[key] = value
        else:
            assert isinstance(value, float)
            self._values[key] = value

    def __delitem__(self, key: int | slice) -> None:
        del self._values[key]

    def __contains__(self, item: object) -> bool:
        return item in self._values

    def __iter__(self) -> Iterator[float]:
        return iter(self._values)

    def __repr__(self) -> str:
        return f"MeasurementSeries({self._values!r})"


class FallbackContainsSequence:
    """Container without ``__contains__``; membership falls back to iteration then ``__getitem__``."""

    def __init__(self, values: list[float]) -> None:
        self._values = list(values)

    def __getitem__(self, index: int) -> float:
        return self._values[index]

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[float]:
        return iter(self._values)


class IndexOnlySequence:
    """Sequence whose ``__getitem__`` requires ``__index__`` conversion."""

    def __init__(self, values: list[str]) -> None:
        self._values = list(values)

    def __getitem__(self, index: int) -> str:
        # ``index`` may be an IndexValue via ``__index__`` protocol used by the runtime
        return self._values[index]

    def __len__(self) -> int:
        return len(self._values)


class MeasurementMap:
    """Mapping-like container distinguishing mapping from sequence."""

    def __init__(self, data: dict[str, float]) -> None:
        self._data = dict(data)

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key: str) -> float:
        return self._data[key]

    def __setitem__(self, key: str, value: float) -> None:
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def keys(self) -> Iterator[str]:
        return iter(self._data.keys())

    def __repr__(self) -> str:
        return f"MeasurementMap({self._data!r})"


def negative_and_slice_demo() -> dict[str, object]:
    """Exercise scalar, negative, slice, and extended-slice access."""

    series = MeasurementSeries([10.0, 20.0, 30.0, 40.0, 50.0])
    last = series[-1]
    sliced = series[1:4]
    extended = series[::2]
    index_obj = IndexValue(1, 99)
    via_index = series[index_obj]  # uses __index__
    return {
        "last": last,
        "sliced": sliced,
        "extended": extended,
        "via_index": via_index,
    }


def contains_fallback_demo() -> tuple[bool, bool]:
    """Show explicit ``__contains__`` versus iteration fallbacks."""

    explicit = MeasurementSeries([1.0, 2.0, 3.0])
    fallback = FallbackContainsSequence([1.0, 2.0, 3.0])
    return (2.0 in explicit), (2.0 in fallback)


def extended_slice_assignment_demo() -> list[float]:
    """Assign and delete through sliced targets."""

    series = MeasurementSeries([1.0, 2.0, 3.0, 4.0, 5.0])
    series[1:3] = [20.0, 30.0]
    del series[::2]
    return list(series)
