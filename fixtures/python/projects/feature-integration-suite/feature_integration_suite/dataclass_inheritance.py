"""Dataclass inheritance with descriptors, slots, and matching (PY-CAN-INT-002)."""

from __future__ import annotations

import dataclasses
import weakref
from dataclasses import dataclass, field
from typing import Any, ClassVar, Generic, TypeVar

T = TypeVar("T")


class GenericDescriptor(Generic[T]):
    """Data descriptor that validates and participates as dataclass field default."""

    _storage: dict[int, Any] = {}

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.name = name
        self.private = f"_{name}_validated"

    def __get__(self, instance: object | None, owner: type[object] | None = None) -> T | GenericDescriptor[T]:
        if instance is None:
            return self
        key = id(instance)
        if key in self._storage:
            return self._storage[key]  # type: ignore[no-any-return]
        return self.default  # type: ignore[no-any-return]

    def __set__(self, instance: object, value: T) -> None:
        if self.expected is not None and not isinstance(value, self.expected):  # type: ignore[attr-defined]
            raise TypeError(f"field {self.name} expects {self.expected}")
        self._storage[id(instance)] = value

    def __delete__(self, instance: object) -> None:
        self._storage.pop(id(instance), None)

    def __init__(self, expected: type[T] | None = None, default: T | None = None) -> None:
        self.expected = expected
        self.default = default  # type: ignore[assignment]


# Shared descriptor instances probed as dataclass defaults
validated_int = GenericDescriptor[int](expected=int, default=0)
validated_label = GenericDescriptor[str](expected=str, default="default-label")


# --- Base / subclass pair exercising field order, slots, frozen, kw_only, weakref, matching ---


@dataclass(slots=True)
class BaseItem:
    """Base dataclass with descriptor-managed field, slots, and ClassVar."""

    identifier: int
    label: str = field(default="base")
    # Descriptor-managed field via default probe: descriptor instance as default value
    # The descriptor instance stored as field default is not invoked as descriptor protocol;
    # instead the field holds the descriptor object itself, demonstrating probe.
    probe: int = field(default=validated_int)  # type: ignore[arg-type]  # descriptor instance as default probe
    total_count: ClassVar[int] = 0

    @property
    def score(self) -> int:  # type: ignore[no-redef]
        return validated_int.__get__(self, type(self))  # type: ignore[no-any-return]

    @score.setter
    def score(self, value: int) -> None:
        validated_int.__set__(self, value)


# Ensure BaseItem supports weakref via slots: need __weakref__ in slots expansion.
# dataclass(slots=True) must include __weakref__ explicitly via slot workaround: we add via `__slots__` not possible after dataclass,
# so we instead provide a slotted base with weakref eligibility via `slots=True` + custom.


@dataclass(slots=True, weakref_slot=True)  # type: ignore[call-arg]  # Python 3.11+ weakref_slot
class SlottedWeakBase:
    value: int = 0

    # `weakref_slot=True` adds __weakref__ so weakref works


@dataclass(slots=True)
class DerivedItem(BaseItem):
    """Subclass adding fields, demonstrating field order, kw_only, and matching exclusion."""

    # New field appears after base fields: field order is base then derived
    extra: int = 0
    # Keyword-only field excluded from positional matching
    note: str = field(default="note", kw_only=True)


@dataclass(slots=True, frozen=True)
class FrozenBase:
    """Frozen base for frozen-write demonstration."""

    identifier: int
    label: str = "frozen"


@dataclass(slots=True, frozen=True)
class FrozenItem(FrozenBase):
    """Frozen subclass to demonstrate frozen-write failure."""

    frozen_extra: int = 0


# Field order demonstration: derived fields appended after base
base_field_order = [f.name for f in dataclasses.fields(BaseItem)]
derived_field_order = [f.name for f in dataclasses.fields(DerivedItem)]

# Descriptor default probe: probe field's default is descriptor instance; property `score` probes descriptor
base_probe_instance = BaseItem(identifier=1)
probe_value = base_probe_instance.score  # should be 0 via descriptor default
descriptor_probe_via_base = base_probe_instance
descriptor_probe_is_int = isinstance(probe_value, int)


# Frozen write failure demo
def frozen_write_failure_demo() -> str:
    item = FrozenItem(identifier=2, label="frozen", frozen_extra=5)
    try:
        item.label = "mutated"  # type: ignore[misc]
        return "no-error"
    except dataclasses.FrozenInstanceError as exc:
        return f"frozen-error:{exc.__class__.__name__}"


# Slot overlap demo: defining duplicate slot name in subclass hierarchy should fail or be deduped?
# Provide a counterexample where subclass tries to redeclare base slot incorrectly.
slot_overlap_note = "DerivedItem slots are merged; duplicate field name would be field-order failure not slot overlap"


def field_order_failure_demo() -> str:
    """Demonstrate field-order failure when non-default follows default in dataclass."""
    try:
        @dataclass
        class BadOrder:
            a: int = 0
            b: int  # type: ignore[valid-type]  # non-default after default

        return "no-error"
    except TypeError as exc:
        return f"field-order-error:{exc}"


# Keyword-only excluded from positional matching demo
def matching_demo() -> dict[str, str]:
    """Structural pattern matching: kw_only field `note` excluded from positional match."""
    item = DerivedItem(identifier=10, label="match", extra=7, note="special")
    item.score = 1
    # probe holds descriptor instance as default value; include it in positional pattern
    probe_val = item.probe  # this is the descriptor instance itself (validated_int)
    # sanity: probe field value is descriptor instance due to descriptor default probe
    _ = probe_val
    # Positional matching: case DerivedItem(10, "match", probe_val, 7) matches base+extra only, not note
    match item:
        case DerivedItem(10, "match", probe_val, 7):
            positional = "matched-pos"
        case _:
            positional = "no-match"

    # Keyword matching includes note
    match item:
        case DerivedItem(identifier=10, note="special"):
            keyword = "matched-kw"
        case _:
            keyword = "no-match"

    # Non-matching case
    match item:
        case DerivedItem(99, _, _, _):
            mismatch = "unexpected"
        case _:
            mismatch = "correctly-unmatched"

    return {"positional": positional, "keyword": keyword, "mismatch": mismatch}


# Weakref demo: slotted dataclass with weakref_slot supports weakref
def weakref_demo() -> dict[str, bool]:
    base = SlottedWeakBase(value=5)
    try:
        r = weakref.ref(base)
        is_alive = r() is base
        base2 = BaseItem(identifier=3)
        # BaseItem slots=True without weakref_slot: weakref should fail
        try:
            r2 = weakref.ref(base2)  # type: ignore[arg-type]
            can_weakref_base = r2() is base2
        except TypeError:
            can_weakref_base = False
        return {"slotted_weakref": is_alive, "base_weakref": can_weakref_base}
    except TypeError as exc:
        return {"error": False, "message": str(exc)}  # type: ignore[return-value]


# Hashing demo: frozen dataclass provides hash
def hashing_demo() -> dict[str, Any]:
    frozen = FrozenItem(identifier=1, label="h", frozen_extra=0)
    try:
        h = hash(frozen)
        return {"hashable": True, "hash": h}
    except TypeError:
        return {"hashable": False}


# Demonstrate all variant callouts in one initializer/match routine
def initialize_and_match_demo() -> dict[str, Any]:
    b = BaseItem(identifier=1, label="base-label")
    b.score = 5
    d = DerivedItem(identifier=2, label="derived", extra=3, note="kw-note")
    d.score = 9
    # mutate via descriptor after init
    b.score = 10
    d.score = 20
    # Check weakref
    wr = weakref_demo()
    # Check matching
    m = matching_demo()
    # Check frozen failure
    fw = frozen_write_failure_demo()
    return {"base_score": b.score, "derived_score": d.score, "weakref": wr, "matching": m, "frozen_write": fw}



