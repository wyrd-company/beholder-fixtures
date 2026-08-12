"""Lazy imports and values (PY-CAN-DYN-010)."""

from __future__ import annotations

import importlib.util
import sys
from functools import cached_property
from types import ModuleType

# Lazy module export via PEP 562 __getattr__ / __dir__ at package level is demonstrated
# by the lazy_submodule module; this file shows per-instance and loader variants.


class HeavyResource:
    """Expensive-to-create object exposed through cached per-instance property."""

    def __init__(self, factor: int) -> None:
        self.factor = factor
        self._load_count = 0

    @cached_property
    def total(self) -> int:
        self._load_count += 1
        # Simulate expensive computation.
        return self.factor * 42

    def load_count(self) -> int:
        return self._load_count


def cached_total(resource: HeavyResource) -> int:
    # First access computes, second returns cached without recompute.
    first = resource.total
    second = resource.total
    assert first == second
    return first


# Lazy loader variant using importlib.util.LazyLoader.
def lazy_import(name: str) -> ModuleType:
    spec = importlib.util.find_spec(name)
    if spec is None or spec.loader is None:
        raise ModuleNotFoundError(name)
    # Loader class mutation: wrap loader in LazyLoader.
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module


# Failure moves to access variant: lazy module that raises on attribute access.
def failing_lazy_module() -> ModuleType:
    mod = ModuleType("dispatch_framework._failing_lazy")

    def __getattr__(name: str) -> object:  # type: ignore[no-redef]
        raise AttributeError(f"lazy load failed for {name!r}")

    mod.__getattr__ = __getattr__  # type: ignore[attr-defined]

    def __dir__() -> list[str]:  # type: ignore[no-redef]
        return ["expected_attr"]

    mod.__dir__ = __dir__  # type: ignore[attr-defined]
    return mod


# Thread-safety and cycle variant: concurrent access shows synchronization change.
import threading


class ThreadSafeLazy:
    """Thread-safe lazy value via lock (contrasts with non-atomic cached_property)."""

    def __init__(self) -> None:
        self._value: int | None = None
        self._lock = threading.Lock()
        self._compute_count = 0

    @property
    def value(self) -> int:
        if self._value is None:
            with self._lock:
                if self._value is None:
                    self._compute_count += 1
                    self._value = 42
        return self._value

    def compute_count(self) -> int:
        return self._compute_count


def concurrent_lazy_access() -> tuple[int, int]:
    lazy = ThreadSafeLazy()
    results: list[int] = []

    def worker() -> None:
        results.append(lazy.value)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return len(set(results)), lazy.compute_count()


class CyclicLazy:
    @cached_property
    def value(self) -> int:
        # Self-reference would recurse; guard shows cycle changes semantics.
        if hasattr(self, "_in_value"):
            return -1
        object.__setattr__(self, "_in_value", True)
        result = self.value  # re-entrant access hits recursion guard
        delattr(self, "_in_value")
        return result if result != -1 else 99


# Stub can expose static surface: __all__ lists lazy names even though they are not yet loaded.
__all__ = ["HeavyResource", "ThreadSafeLazy", "cached_total", "lazy_import", "concurrent_lazy_access", "failing_lazy_module"]


def __dir__() -> list[str]:
    return sorted(__all__)
