"""Static-only imports and forward references (PY-CAN-TYPE-021)."""

from __future__ import annotations

from typing import TYPE_CHECKING, get_type_hints

if TYPE_CHECKING:
    from typed_toolkit.cycle_a import Batch as CycleBatchA

if TYPE_CHECKING:
    from typing import TypedDict as TDForChecking

# Both spellings of TYPE_CHECKING used above (direct import and string form
# via ``typing.TYPE_CHECKING`` would be the alternative; here we demonstrate
# the imported constant form).

# Use typing.TYPE_CHECKING spelling in a second conditional block
import typing

if typing.TYPE_CHECKING:
    from typed_toolkit.cycle_b import Record as CycleRecordB


# --- Break real import cycle with TYPE_CHECKING -------------------------------

def create_batch(label: str) -> CycleBatchA:  # type: ignore[valid-type]
    from typed_toolkit.cycle_a import Batch

    return Batch(label)


def create_record(value: int) -> CycleRecordB:  # type: ignore[valid-type]
    from typed_toolkit.cycle_b import Record

    return Record(value)


# --- Runtime name absent variant ----------------------------------------------

def runtime_name_absent_demo() -> bool:
    # ``CycleBatchA`` is not available at runtime; TYPE_CHECKING guard ensures
    # no import is attempted unless checking.
    return "CycleBatchA" not in globals()


# --- Quoted / postponed annotation variant ------------------------------------

def quoted_annotation(value: "CycleBatchA") -> "CycleBatchA":  # type: ignore[no-redef]
    return value


def postponed_annotation_demo(value: CycleBatchA) -> CycleBatchA:  # type: ignore[valid-type]
    # Under ``from __future__ import annotations`` this annotation is stringized
    # and not evaluated at definition time.
    return value


# --- Explicit namespace resolution with get_type_hints ------------------------

def resolve_with_explicit_namespaces() -> dict[str, object]:
    from typed_toolkit.cycle_a import Batch

    def holder(item: Batch) -> Batch:
        return item

    # Provide explicit namespaces to resolve the stringized annotation.
    return get_type_hints(holder, globalns={"Batch": Batch})


# --- Base and decorator still need runtime import (assigned variant) -----------

# Base classes and decorators are evaluated at runtime even under postponed
# annotations, so they cannot be guarded by TYPE_CHECKING alone.

from typed_toolkit.cycle_a import Batch as RuntimeBatch


class DerivedBatch(RuntimeBatch):
    extra: str = "derived"


def _runtime_decorator(cls: type) -> type:  # type: ignore[no-untyped-def]
    cls._decorated = True  # type: ignore[attr-defined]
    return cls


# Decorator must be imported at runtime (not inside TYPE_CHECKING) and applied
# at definition time; postponed annotations do not defer decorator evaluation.
@_runtime_decorator
class DecoratedBatch(RuntimeBatch):
    tag: str = "decorated"


def decorator_needs_runtime() -> type[DecoratedBatch]:
    return DecoratedBatch


def base_and_decorator_runtime_demo() -> tuple[bool, bool]:
    return issubclass(DerivedBatch, RuntimeBatch), getattr(DecoratedBatch, "_decorated", False)
