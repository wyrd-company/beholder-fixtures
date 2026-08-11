"""Variable and annotation-only declarations (PY-CAN-TYPE-002)."""

from __future__ import annotations

from typing import ClassVar

# --- Module scope: with and without values ----------------------------------

module_label: str = "inventory"
module_pending: int  # annotation without value: metadata without binding
module_union: str | int = 42


# --- Class scope --------------------------------------------------------------

class Record:
    # Class variable with value
    category: str = "general"
    # Class variable annotation-only (no binding at runtime)
    pending_class_value: int
    # ClassVar indicates class-only storage
    instances_created: ClassVar[int] = 0
    # Instance annotation (collected via __annotations__ but not auto-collected
    # as instance dict entry without assignment)
    instance_label: str
    instance_count: int

    def __init__(self, label: str, count: int) -> None:
        self.instance_label = label
        self.instance_count = count
        Record.instances_created += 1


# --- Instance annotations not automatically collected -------------------------

def instance_annotation_collection_demo() -> tuple[dict, dict]:
    r = Record("widget", 3)
    # ``__annotations__`` on the class holds all declared names; instance
    # ``__dict__`` holds only assigned values.
    return dict(Record.__annotations__), dict(r.__dict__)


# --- Local scope classification ----------------------------------------------

def local_annotations(flag: bool) -> dict[str, str]:
    local_pending: str  # local annotation-only: no binding unless assigned
    if flag:
        local_pending = "assigned"
    else:
        local_pending = "fallback"
    local_with_value: int = 10
    return {"pending": local_pending, "value": str(local_with_value)}


def local_compiler_classification() -> tuple[tuple[str, ...], str]:
    """Show local compiler classification via code object varnames."""
    def inner() -> str:
        annotated_local: str = "hello"
        return annotated_local
    return inner.__code__.co_varnames, inner()


# --- Non-simple target variant ------------------------------------------------

# Annotation on attribute and subscript targets (not just simple names).
class Container:
    def __init__(self) -> None:
        self.items: list[str] = []


def annotate_attribute_target() -> list[str]:
    c = Container()
    c.items: list[str] = ["a", "b"]  # type: ignore[no-redef]
    return c.items


def annotate_subscript_target() -> dict[str, int]:
    mapping: dict[str, int] = {}
    mapping["key"]: int = 99  # type: ignore[no-redef]
    return mapping


# --- Metadata without binding -------------------------------------------------

# Accessing ``__annotations__`` shows metadata even where no value exists.
def metadata_without_binding() -> dict[str, object]:
    return dict(Record.__annotations__)
