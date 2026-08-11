"""Caching wrappers and cached properties (PY-CAN-CALL-009)."""

from __future__ import annotations

import functools
from functools import cached_property

call_count = 0


@functools.lru_cache(maxsize=32)
def cached_weight(label: str, factor: int = 2) -> int:
    """LRU-cache wrapper with identity and ``__wrapped__``."""

    global call_count
    call_count += 1
    return len(label) * factor


@functools.cache
def simple_cache(label: str) -> str:
    """Unbounded ``cache`` alias (Python 3.9+)."""

    return label.upper()


class Shipment:
    """Class exercising ``cached_property`` as a non-data descriptor."""

    def __init__(self, code: str) -> None:
        self.code = code
        self._compute_calls = 0

    @cached_property
    def manifest(self) -> str:
        """Cached manifest derived from ``code``."""

        self._compute_calls += 1
        return f"manifest:{self.code}:{self._compute_calls}"


class SlottedShipment:
    """``__slots__`` without ``__dict__`` — ``cached_property`` cannot cache."""

    __slots__ = ("code",)

    def __init__(self, code: str) -> None:
        self.code = code

    @cached_property  # type: ignore[no-redef]
    def manifest(self) -> str:  # type: ignore[override]
        return f"slotted:{self.code}"


def cache_identity_and_state() -> dict[str, object]:
    """Expose cache identity, hits, and invalidation."""

    global call_count
    call_count = 0
    cached_weight.cache_clear()
    first = cached_weight("parcel", 2)
    second = cached_weight("parcel", 2)
    info_before = cached_weight.cache_info()
    cached_weight("other", 2)
    info_after = cached_weight.cache_info()
    return {
        "first": first,
        "second": second,
        "call_count": call_count,
        "hits_before": info_before.hits,
        "misses_before": info_before.misses,
        "currsize_after": info_after.currsize,
        "wrapped": hasattr(cached_weight, "__wrapped__"),
    }


def wrapped_access() -> object:
    """Access the wrapped function through ``__wrapped__``."""

    return cached_weight.__wrapped__  # type: ignore[attr-defined]


def non_data_descriptor_shadowing() -> dict[str, object]:
    """``cached_property`` is a non-data descriptor: instance dict shadows it."""

    shipment = Shipment("AB-12")
    first = shipment.manifest
    # Shadowing via instance dict.
    shipment.__dict__["manifest"] = "overridden"
    shadowed = shipment.manifest
    del shipment.__dict__["manifest"]
    recomputed = shipment.manifest
    return {
        "first": first,
        "shadowed": shadowed,
        "recomputed": recomputed,
        "calls": shipment._compute_calls,
    }


def slots_without_dict_failure() -> str:
    """``cached_property`` on a slotted class without ``__dict__`` raises on access."""

    slotted = SlottedShipment("SX-01")
    try:
        _ = slotted.manifest
        return "no-error"
    except TypeError:
        return "type-error"
    except AttributeError:
        return "attribute-error"


def concurrency_caveat_note() -> str:
    """Exact concurrency semantics for the caching wrappers."""

    return (
        "lru_cache keeps its cache coherent across threads but the wrapped "
        "function may be invoked more than once when two threads miss concurrently; "
        "cached_property may likewise compute more than once per instance on "
        "concurrent first access"
    )


def cache_clear_and_invalidate() -> dict[str, int]:
    """Drive cache invalidation and report sizes."""

    cached_weight.cache_clear()
    cached_weight("alpha", 1)
    cached_weight("beta", 1)
    before = cached_weight.cache_info().currsize
    cached_weight.cache_clear()
    after = cached_weight.cache_info().currsize
    return {"before": before, "after": after}
