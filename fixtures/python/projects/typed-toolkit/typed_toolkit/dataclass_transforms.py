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


# --- Transform-decorated decorator -------------------------------------------

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


# --- Checker divergence and advertised/runtime drift note ---------------------

# A checker sees ``@create_model`` and assumes dataclass semantics.  If the
# runtime decorator failed to call ``dataclasses.dataclass``, the advertised
# ``__init__`` would drift from runtime reality.  Here they align.
def advertised_runtime_drift_note() -> bool:
    return hasattr(InventoryModel, "__dataclass_fields__") and hasattr(BatchRecord, "__dataclass_fields__")
