"""Self types and overrides (PY-CAN-TYPE-013)."""

from __future__ import annotations

from typing import Self, override

# --- Fluent instance methods returning Self ----------------------------------

class Batch:
    def __init__(self, label: str, count: int = 0) -> None:
        self.label = label
        self.count = count

    def with_label(self, label: str) -> Self:
        self.label = label
        return self

    def with_count(self, count: int) -> Self:
        self.count = count
        return self

    @classmethod
    def create(cls, label: str) -> Self:
        return cls(label)

    def clone(self) -> Self:
        return type(self)(self.label, self.count)


class SpecialBatch(Batch):
    def __init__(self, label: str, count: int = 0, priority: int = 0) -> None:
        super().__init__(label, count)
        self.priority = priority

    def with_priority(self, priority: int) -> Self:
        self.priority = priority
        return self


def self_subclass_specialization_demo() -> SpecialBatch:
    # ``Self`` resolves to the subclass when called on the subclass.
    b = SpecialBatch("widget").with_label("gadget").with_priority(5)
    return b


# --- Explicit self-type alternative -------------------------------------------

from typing import TypeVar

TBatch = TypeVar("TBatch", bound=Batch)


def explicit_self_type(batch: TBatch, label: str) -> TBatch:
    batch.label = label
    return batch


# --- @override valid and invalid variants ------------------------------------

class BaseHandler:
    def handle(self, value: str) -> str:
        return value.upper()

    def describe(self) -> str:
        return "base"


class ValidOverride(BaseHandler):
    @override
    def handle(self, value: str) -> str:
        return f"valid:{value}"

    @override
    def describe(self) -> str:
        return "valid-override"


# Invalid override: checker would flag misspelled base member name.
class InvalidOverride(BaseHandler):
    @override  # type: ignore[arg-type]
    def handle_typo(self, value: str) -> str:  # not in base: checker error
        return value

    @override  # type: ignore[arg-type]
    def descibe(self) -> str:  # misspelled
        return "typo"


# --- Decorator order and metadata variant ------------------------------------

def tag_decorator(func):  # type: ignore[no-untyped-def]
    func._tagged = True  # type: ignore[attr-defined]
    return func


class OrderDemo(BaseHandler):
    @tag_decorator
    @override
    def handle(self, value: str) -> str:
        return value.lower()

    @override
    @tag_decorator
    def describe(self) -> str:
        return "order-demo"


def decorator_order_demo() -> tuple[bool, bool]:
    a = OrderDemo()
    return getattr(a.handle, "_tagged", False), getattr(a.describe, "_tagged", False)
