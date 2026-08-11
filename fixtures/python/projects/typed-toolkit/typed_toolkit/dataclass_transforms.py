"""Dataclass transforms (PY-CAN-TYPE-018)."""

from __future__ import annotations

import dataclasses
from typing import dataclass_transform, TypeVar

T = TypeVar("T")

# --- Field specifiers ---------------------------------------------------------

def model_field(*, default: object = dataclasses.MISSING, default_factory=dataclasses.MISSING, init: bool = True):  # type: ignore[no-untyped-def]
    if default is not dataclasses.MISSING and default_factory is not dataclasses.MISSING:
        raise ValueError("cannot specify both default and default_factory")
    return dataclasses.field(default=default, default_factory=default_factory, init=init)  # type: ignore[arg-type]


# --- Transform-decorated decorator (real runtime is dataclass) ---------------

@dataclass_transform(field_specifiers=(model_field, dataclasses.field))
def create_model(cls: type[T]) -> type[T]:
    """A decorator that provides dataclass-like behavior at type-check time."""
    return dataclasses.dataclass(cls)  # type: ignore[return-value]


@create_model
class InventoryModel:
    label: str
    quantity: int = model_field(default=0)
    unit: str = model_field(default="pcs")


# --- Transform-decorated base class ------------------------------------------

@dataclass_transform(field_specifiers=(dataclasses.field,))
class ModelBase:
    """Base class whose subclasses get dataclass-like treatment."""

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        dataclasses.dataclass(cls)  # type: ignore[arg-type]


class BatchRecord(ModelBase):
    label: str
    quantity: int
    notes: str = dataclasses.field(default="")


# --- Transform-decorated metaclass -------------------------------------------

@dataclass_transform(field_specifiers=(dataclasses.field,))
class ModelMeta(type):
    def __new__(mcls, name: str, bases: tuple[type, ...], ns: dict[str, object], **kw: object) -> type:  # type: ignore[no-untyped-def]
        cls = super().__new__(mcls, name, bases, ns)  # type: ignore[arg-type]
        return dataclasses.dataclass(cls)  # type: ignore[return-value, arg-type]


class MetaModel(metaclass=ModelMeta):
    label: str
    value: int = dataclasses.field(default=0)


class ConcreteMeta(MetaModel):
    extra: str = dataclasses.field(default="none")


# --- Divergent transform (advertised dataclass but runtime is plain class) ----
# A checker treats this as a dataclass with generated ``__init__``, but at
# runtime the decorator does not call ``dataclasses.dataclass``, so the
# advertised init contract diverges and ``__dataclass_fields__`` is absent.

@dataclass_transform(field_specifiers=(dataclasses.field,))
def advertise_only(cls: type[T]) -> type[T]:
    # Intentionally not calling dataclasses.dataclass at runtime.
    return cls


@advertise_only
class DivergentModel:
    label: str
    quantity: int = dataclasses.field(default=0)


def divergent_runtime_check() -> bool:
    return not hasattr(DivergentModel, "__dataclass_fields__")


def advertised_vs_real_init() -> tuple[bool, bool]:
    # ``InventoryModel`` has real dataclass fields, ``DivergentModel`` does not.
    return hasattr(InventoryModel, "__dataclass_fields__"), hasattr(DivergentModel, "__dataclass_fields__")


# --- Static defaults versus runtime overrides ---------------------------------

def static_defaults_vs_runtime_demo() -> tuple[InventoryModel, BatchRecord]:
    # Checker assumes ``InventoryModel(label=...)`` requires ``label``; runtime
    # dataclass enforces ``__init__`` accordingly.  Overriding defaults at
    # runtime still works but diverges from static expectation if misused.
    a = InventoryModel(label="widget", quantity=5)
    b = BatchRecord(label="gadget", quantity=10)
    b.quantity = 99  # runtime override after construction
    return a, b


# --- Generated initializer contract variant -----------------------------------

def generated_init_contract_demo() -> str:
    # ``create_model`` claims to generate ``__init__(label: str, quantity: int, unit: str)``
    # The dataclass machinery actually provides it.
    m = InventoryModel(label="a", quantity=1, unit="kg")
    return m.label


# --- Checker divergence and advertised/runtime drift --------------------------

def advertised_runtime_drift_note() -> bool:
    # Real drift between advertised transform contract and runtime reality,
    # plus checker divergence where static and runtime disagree.
    return hasattr(InventoryModel, "__dataclass_fields__") and not hasattr(DivergentModel, "__dataclass_fields__")
