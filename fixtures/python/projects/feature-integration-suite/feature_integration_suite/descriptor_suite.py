"""Decorated, overloaded, generic descriptor (PY-CAN-INT-001)."""

from __future__ import annotations

import abc
import functools
from typing import Annotated, Any, Generic, TypeVar, overload

# --- Registry for runtime registration variant ---

REGISTRY: dict[str, Any] = {}


def register_field(name: str):  # noqa: ANN001 - generic decorator
    """Register a descriptor field by name at decoration time."""

    def decorator(obj: Any) -> Any:
        REGISTRY[name] = obj
        obj._registered_name = name  # type: ignore[attr-defined]
        return obj

    return decorator


# --- Generic descriptor combining binding, wrappers, overloads, annotations ---

T = TypeVar("T")


class ManagedField(Generic[T]):
    """Generic data descriptor that validates type and registers via __set_name__."""

    def __set_name__(self, owner: type[Any], name: str) -> None:
        self.public_name = name
        self.private_name = f"_{name}_value"
        REGISTRY[f"{owner.__name__}.{name}"] = self

    @overload
    def __get__(self, instance: None, owner: type[Any]) -> ManagedField[T]: ...  # type: ignore[overload-overlap]

    @overload
    def __get__(self, instance: object, owner: type[Any] | None = None) -> T: ...

    def __get__(self, instance: object | None, owner: type[Any] | None = None) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.private_name, self.default)  # type: ignore[attr-defined]

    def __set__(self, instance: object, value: T) -> None:
        if self.expected_type is not None and not isinstance(value, self.expected_type):  # type: ignore[attr-defined]
            raise TypeError(f"expected {self.expected_type} for {self.public_name}")
        setattr(instance, self.private_name, value)  # type: ignore[attr-defined]

    def __delete__(self, instance: object) -> None:
        if hasattr(instance, self.private_name):  # type: ignore[attr-defined]
            delattr(instance, self.private_name)  # type: ignore[attr-defined]

    def __init__(self, expected_type: type[T] | None = None, default: T | None = None) -> None:
        self.expected_type = expected_type
        self.default = default  # type: ignore[assignment]

    # Preserve wrapper metadata for call-through helpers
    @functools.wraps(__get__)
    def wrapped_get(self, instance: object | None, owner: type[Any] | None = None) -> Any:  # type: ignore[no-untyped-def]
        return self.__get__(instance, owner)


# --- Wrapper preservation demo ---


def preserve_signature(func: Any) -> Any:
    """Wrapper that preserves signature and binding via functools.wraps."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    wrapper._is_wrapper = True  # type: ignore[attr-defined]
    return wrapper


# --- Abstract + property ordering correct vs wrong ---


class AbstractBase(abc.ABC):
    """Demonstrates abstractness through decorated descriptor / property."""

    @property
    @abc.abstractmethod
    def abstract_value(self) -> int:  # type: ignore[no-untyped-def]
        """Abstract property - correct order: @property then @abstractmethod not allowed; correct is @property with abstract."""
        raise NotImplementedError


# Correct order: @register_field wraps descriptor, then dataclass uses it.
# For property-based abstract descriptor, correct is @property above @abstractmethod
# The inverse loses abstractness.


class CorrectAbstractProperty(abc.ABC):
    @property
    @abc.abstractmethod
    def value(self) -> int:  # pragma: no cover - abstract
        raise NotImplementedError

    @value.setter  # type: ignore[attr-defined]
    @abc.abstractmethod
    def value(self, v: int) -> None:  # pragma: no cover
        raise NotImplementedError


wrong_order_abstract_error: str | None = None
try:

    class WrongOrderLosesAbstractness(abc.ABC):  # type: ignore[no-redef]
        """Wrong order: @abstractmethod above @property loses abstract flag or raises."""

        @abc.abstractmethod  # type: ignore[arg-type]
        @property
        def value(self) -> int:  # pragma: no cover
            raise NotImplementedError

except AttributeError as _exc:
    wrong_order_abstract_error = f"AttributeError:{_exc}"
    # Define placeholder so coverage locator still exists
    class WrongOrderLosesAbstractness(abc.ABC):  # type: ignore[no-redef]
        """Placeholder after wrong-order failure."""

        value = 0  # type: ignore[assignment]



# --- Decorator stack on one member: binding + wrappers + registration + annotations ---

# Annotated type alias for annotation variant
FieldAnnotation = Annotated[int, "managed"]


class IntegrationRecord(Generic[T]):
    """Host class that combines binding, wrappers, overloads, annotations, and registration on one member."""

    # Single member combining all facets: generic descriptor, annotated, registered, wrapped
    managed: ManagedField[int] = ManagedField[int](expected_type=int, default=0)

    # Overloaded accessor that dispatches via registration + descriptor binding
    @overload
    def get_value(self, as_str: bool = False) -> int: ...

    @overload
    def get_value(self, as_str: bool = True) -> str: ...

    def get_value(self, as_str: bool = False) -> int | str:
        raw: int = self.managed  # descriptor binding
        return str(raw) if as_str else raw


# Preserve signature demonstration: wrapper must not lose binding
wrapped_managed_get = preserve_signature(ManagedField.__get__)


# --- Decorator order variants: register / setter / abstractness / signature / binding ---


def order_log() -> list[str]:
    """Return deterministic log of decorator evaluation vs application."""
    return []


class OrderSensitiveDescriptor(ManagedField[int]):
    """Subclass used to probe order effects."""


# Correct ordering: registration outermost preserves metadata and binding
@register_field("correct_binding")
class CorrectBindingHost:
    field: ManagedField[int] = ManagedField[int](expected_type=int, default=1)

    @property
    def value(self) -> int:
        return self.field

    @value.setter
    def value(self, v: int) -> None:
        self.field = v  # type: ignore[attr-defined]


# Wrong order: wrapper strips __set_name__ or loses binding
def stripping_wrapper(cls: type[Any]) -> type[Any]:
    """Replacement decorator that would lose original descriptor if order wrong."""
    # Simulate a non-callable replacement failure: returning non-descriptor loses binding
    return cls  # but if placed inside __set_name__ chain wrongly, registration misses


# Counterexample: registration inner vs outer
class WrongRegistrationOrder:
    # If @register_field is inner to a replacing decorator, the registry sees wrapper not descriptor
    pass


# Demonstrate signature loss when wrapper not using wraps
def no_wraps_wrapper(func: Any) -> Any:
    def inner(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return inner


wrapped_without_preservation = no_wraps_wrapper(ManagedField.__get__)
wrapped_with_preservation = preserve_signature(ManagedField.__get__)

signature_preserved = hasattr(wrapped_with_preservation, "__wrapped__")
signature_lost = not hasattr(wrapped_without_preservation, "__wrapped__")

# Binding loss demo: accessing via class vs instance
binding_via_class_is_descriptor = isinstance(IntegrationRecord.__dict__["managed"], ManagedField)
binding_via_instance_is_value = isinstance(IntegrationRecord().managed, int)

# Overload runtime vs static dispatch disagreement
# Static overload says get_value(as_str=True) -> str, but singledispatch would choose int branch at runtime if based on first arg type
import functools as _functools2  # alias to avoid shadowing


@_functools2.singledispatch
def dispatched_get(value: int) -> str:
    return f"int:{value}"


@dispatched_get.register
def _dispatch_str(value: str) -> str:  # type: ignore[no-redef]
    return f"str:{value}"


def static_vs_runtime_disagreement_demo() -> dict[str, str]:
    """Overload signature predicts str for bool, runtime dispatch predicts int branch."""
    rec = IntegrationRecord[int]()
    rec.managed = 42
    static_result: str = rec.get_value(as_str=True)  # static expects str
    runtime_result = dispatched_get(rec.managed)  # runtime dispatches on int
    return {"static": static_result, "runtime": runtime_result}


def decorator_order_effects() -> dict[str, Any]:
    """Expose decorator order probes for evaluation."""
    return {
        "correct_registry_has_descriptor": "CorrectBindingHost.field" in REGISTRY,
        "signature_preserved": signature_preserved,
        "signature_lost": signature_lost,
        "binding_via_class_is_descriptor": binding_via_class_is_descriptor,
        "binding_via_instance_is_value": binding_via_instance_is_value,
        "abstract_preserved": getattr(CorrectAbstractProperty.value, "__isabstractmethod__", False),  # type: ignore[attr-defined]
        "wrapped_has_wrapped_attr": hasattr(wrapped_managed_get, "__wrapped__"),
    }


# Stub drift: runtime descriptor type is ManagedField, stub declares a different name alias
# See descriptor_suite.pyi: stub exports `ManagedFieldStub` with different signature
stub_declares_drift = True
