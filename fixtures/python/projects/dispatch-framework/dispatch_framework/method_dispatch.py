"""Single-dispatch methods (PY-CAN-DYN-002)."""

from __future__ import annotations

from functools import singledispatchmethod


class ChannelDispatcher:
    """Dispatch on first non-receiver argument for instance/class/static variants."""

    # Instance method variant: singledispatchmethod must be outer decorator.
    @singledispatchmethod
    def deliver(self, payload: object) -> str:
        return f"default:{type(payload).__name__}"

    @deliver.register(int)
    def _deliver_int(self, payload: int) -> str:
        return f"int:{payload}"

    @deliver.register(str)
    def _deliver_str(self, payload: str) -> str:
        return f"str:{payload!r}"

    # Annotation-inferred registration on method.
    @deliver.register
    def _deliver_float(self, payload: float) -> str:
        return f"float:{payload:.1f}"

    # Descriptor binding variant: method accessed via instance vs class shows binding.
    def bound_deliver(self, payload: object) -> str:
        return self.deliver(payload)

    # Class dispatch variant: dispatch on first non-cls argument.
    @singledispatchmethod
    @classmethod
    def create(cls, spec: object) -> str:
        return f"create-default:{type(spec).__name__}"

    @create.register(dict)
    @classmethod
    def _create_dict(cls, spec: dict) -> str:
        return f"create-dict:{sorted(spec.keys())!r}"

    # Static dispatch variant: dispatch on first argument (no receiver).
    @singledispatchmethod
    @staticmethod
    def transform(value: object) -> str:
        return f"transform-default:{type(value).__name__}"

    @transform.register(list)
    @staticmethod
    def _transform_list(value: list) -> str:
        return f"transform-list:{len(value)}"


# Decorator order controls .register: correct order is singledispatchmethod outermost.
# Wrong order (commented) would break: @classmethod @singledispatchmethod is invalid.
class CorrectOrder:
    @singledispatchmethod
    @classmethod
    def handle(cls, item: object) -> str:
        return "default"

    @handle.register(int)
    @classmethod
    def _handle_int(cls, item: int) -> str:
        return f"int:{item}"


# Inheritance and later registration variant.
class BaseHandler:
    @singledispatchmethod
    def process(self, arg: object) -> str:
        return "base-default"

    @process.register(int)
    def _process_int(self, arg: int) -> str:
        return f"base-int:{arg}"


class DerivedHandler(BaseHandler):
    # Inherits dispatch; extra registration after base definition.
    @BaseHandler.process.register(str)  # type: ignore[attr-defined]
    def _process_str(self, arg: str) -> str:
        return f"derived-str:{arg!r}"


# Later registration patching existing dispatcher.
def extend_base_with_float() -> None:
    @BaseHandler.process.register(float)  # type: ignore[attr-defined]
    def _process_float(self: BaseHandler, arg: float) -> str:
        return f"base-float:{arg:.2f}"

    # Function exists so later registration is explicit.
    _ = _process_float
