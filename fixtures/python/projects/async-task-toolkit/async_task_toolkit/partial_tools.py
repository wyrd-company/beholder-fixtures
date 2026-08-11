"""``partial`` and ``partialmethod`` (PY-CAN-CALL-008)."""

from __future__ import annotations

import functools
import inspect
from typing import Any, Callable


def scale_payload(value: int, factor: int, offset: int = 0) -> int:
    """Base callable for partial derivation."""

    return value * factor + offset


# Module-level partials.
double = functools.partial(scale_payload, factor=2)
double_with_offset = functools.partial(scale_payload, factor=2, offset=5)


def bound_method_partial() -> dict[str, object]:
    """Create a ``partial`` from a bound method and inspect exposed ``.func``."""

    class Scaler:
        def method(self, value: int, factor: int) -> int:
            return value * factor

    bound = Scaler().method
    partial_from_bound = functools.partial(bound, 10)
    return {
        "result": partial_from_bound(factor=3),
        "func": partial_from_bound.func,
        "func_is_bound": hasattr(partial_from_bound.func, "__self__"),
        "args": partial_from_bound.args,
        "keywords": partial_from_bound.keywords,
    }


class ParcelBatch:
    """Expose descriptor-bound callables via ``partialmethod``."""

    def _apply(self, label: str, *, priority: int = 1) -> str:
        return f"{label}:{priority}"

    prioritized = functools.partialmethod(_apply, priority=5)
    labeled = functools.partialmethod(_apply, label="parcel")


def partialmethod_descriptor_behavior() -> dict[str, object]:
    """Access ``partialmethod`` through class and instance."""

    batch = ParcelBatch()
    return {
        "via_instance_with_override": batch.prioritized(label="alpha"),
        "via_instance_default_label": batch.labeled(),
        "via_class_is_descriptor": isinstance(ParcelBatch.__dict__["prioritized"], functools.partialmethod),
        "wiring": batch.prioritized.__self__ if hasattr(batch.prioritized, "__self__") else None,  # type: ignore[attr-defined]
    }


def exposed_func_attribute() -> Callable[..., Any] | None:
    """Show that ``partial`` exposes ``.func``, ``.args``, and ``.keywords``."""

    return double.func  # type: ignore[return-value]


def signature_introspection_differences() -> dict[str, object]:
    """Contrast signatures between original, partial, and partialmethod."""

    original_sig = inspect.signature(scale_payload)
    partial_sig = inspect.signature(double)
    # partial's signature still reflects underlying, but functools does not fully remove bound args.
    batch_sig = inspect.signature(ParcelBatch.prioritized)
    return {
        "original": str(original_sig),
        "partial": str(partial_sig),
        "partial_func": double.func.__name__,
        "partial_has_keywords": double.keywords,
        "partialmethod_descriptor": type(ParcelBatch.__dict__["prioritized"]).__name__,
        "batch_sig": str(batch_sig),
    }

