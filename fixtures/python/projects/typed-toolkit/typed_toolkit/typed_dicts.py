"""Typed dictionaries (PY-CAN-TYPE-010)."""

from __future__ import annotations

from typing import NotRequired, ReadOnly, Required, TypedDict

# --- Class-based TypedDict ----------------------------------------------------

class InventoryRecord(TypedDict):
    label: str
    quantity: int


class InventoryRecordWithTotal(TypedDict, total=True):
    label: str
    quantity: int
    unit: str


class InventoryRecordPartial(TypedDict, total=False):
    label: str
    quantity: int


# --- Functional form ----------------------------------------------------------

FunctionalRecord = TypedDict("FunctionalRecord", {"label": str, "quantity": int})
FunctionalWithRequired = TypedDict(
    "FunctionalWithRequired",
    {"label": str, "notes": NotRequired[str]},
)


# --- Inheritance --------------------------------------------------------------

class BaseRecord(TypedDict):
    label: str


class ExtendedRecord(BaseRecord):
    quantity: int


class FurtherExtended(ExtendedRecord, total=False):
    notes: str


# --- Totality and per-key requiredness ---------------------------------------

class MixedRequiredness(TypedDict):
    required_field: Required[str]
    optional_field: NotRequired[int]
    normal_field: str


def mixed_requiredness_demo() -> MixedRequiredness:
    return {"required_field": "a", "normal_field": "b"}


# --- Read-only and open / extra-key variants ---------------------------------

class ReadOnlyRecord(TypedDict):
    label: ReadOnly[str]
    quantity: int


# ``closed`` and ``extra_items`` are typing-spec extensions for TypedDict
# (PEP 728).  They are not yet implemented in the stdlib ``typing`` on
# CPython 3.14, so the precise syntax is shown as a comment variant and
# would be checked by a type checker:
# class OpenRecord(TypedDict, closed=False): ...
# class ClosedRecord(TypedDict, closed=True): ...
# class ExtraKeysRecord(TypedDict, extra_items=int): ...
# The following runtime representatives use the available ``total`` forms.
class ClosedLikeRecord(TypedDict, total=True):
    label: str


class OpenLikeRecord(TypedDict, total=False):
    label: str


# --- Plain runtime dictionary (no typing enforcement) -------------------------

def plain_dict_is_typed_dict() -> InventoryRecord:
    # At runtime a TypedDict is just a dict; any dict with matching keys works.
    data: InventoryRecord = {"label": "widget", "quantity": 5}
    return data


def plain_runtime_dict_demo() -> dict[str, object]:
    raw: dict[str, object] = {"label": "gadget", "quantity": 10, "extra": True}
    typed: InventoryRecord = raw  # type: ignore[assignment]
    return typed  # type: ignore[return]


# --- No runtime instance check variant ----------------------------------------

def no_runtime_instance_check_demo() -> str:
    try:
        isinstance({"label": "x"}, InventoryRecord)  # type: ignore[arg-type]
        return "no-error"
    except TypeError as exc:
        return f"TypeError:{exc}"


# --- Invalid identifiers note -------------------------------------------------

# TypedDict with invalid identifier keys must use functional syntax:
WeirdKeys = TypedDict("WeirdKeys", {"with-dash": str, "123start": int})


# --- Metadata variant ---------------------------------------------------------

def typed_dict_metadata_demo() -> dict[str, object]:
    return {
        "annotations": dict(InventoryRecord.__annotations__),
        "required_keys": getattr(InventoryRecord, "__required_keys__", None),
        "optional_keys": getattr(InventoryRecord, "__optional_keys__", None),
        "total": getattr(InventoryRecord, "__total__", None),
    }
