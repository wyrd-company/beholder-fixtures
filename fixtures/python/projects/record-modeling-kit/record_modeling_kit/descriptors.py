"""Data and non-data descriptors (PY-CAN-OBJ-006)."""

from __future__ import annotations

from typing import Any


class ValidatingDescriptor:
    """Data descriptor that validates and stores per-instance."""

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.private_name = f"_{name}_validated"

    def __get__(self, instance: object | None, owner: type | None = None) -> Any:
        if instance is None:
            return self
        if self.private_name not in instance.__dict__:
            raise AttributeError(f"{self.name} not set")
        return instance.__dict__[self.private_name]

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("value must be non-negative int")
        instance.__dict__[self.private_name] = value

    def __delete__(self, instance: object) -> None:
        if self.private_name in instance.__dict__:
            del instance.__dict__[self.private_name]
        else:
            raise AttributeError(f"{self.name} not set")


class CachedDescriptor:
    """Non-data cached descriptor (stores computed value on first access)."""

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.cache_name = f"_{name}_cached"

    def __get__(self, instance: object | None, owner: type | None = None) -> Any:
        if instance is None:
            return self
        if self.cache_name not in instance.__dict__:
            # Simulate expensive computation.
            instance.__dict__[self.cache_name] = f"computed-{self.name}"
        return instance.__dict__[self.cache_name]


class DescriptorOwner:
    count = ValidatingDescriptor()
    label = CachedDescriptor()


# Reused descriptor instance across two classes.
shared_validating = ValidatingDescriptor()


class OwnerA:
    shared = shared_validating


class OwnerB:
    shared = shared_validating


def instance_collision_demo() -> tuple[str, str]:
    """Instance dict collision: non-data loses, data wins."""

    class NonData:
        value = CachedDescriptor()

    obj = NonData()
    # Shadow non-data descriptor via instance dict.
    obj.__dict__["value"] = "instance-value"
    shadowed = obj.value  # instance dict wins for non-data
    # Data descriptor ignores instance dict for read.
    dobj = DescriptorOwner()
    dobj.count = 5
    dobj.__dict__["count"] = 999  # will be ignored? data descriptor shadows
    # But we stored under private name; __dict__ entry "count" is separate.
    data_val = dobj.count
    return shadowed, str(data_val)  # type: ignore[return-value]


def set_name_demo() -> tuple[str, str]:
    return DescriptorOwner.count.name, DescriptorOwner.label.name  # type: ignore[attr-defined]


def reuse_demo() -> bool:
    return OwnerA.shared is OwnerB.shared


class OwnerWithFallback:
    count = ValidatingDescriptor()

    def __getattr__(self, name: str) -> str:
        if name == "count":
            return "fallback-via-getattr"
        raise AttributeError(name)


def attribute_error_fallback_demo() -> str:
    # Descriptor raises AttributeError -> owner __getattr__ provides fallback via normal lookup.
    obj = OwnerWithFallback()
    return obj.count  # type: ignore[return-value]


# Functions, slots, and properties as descriptor contrasts.
class ContrastDemo:
    def func(self) -> str:
        return "method"

    __slots__ = ("slot_val",)

    @property
    def prop(self) -> str:
        return "prop-value"


def descriptor_contrast_demo() -> tuple[str, str, str]:
    obj = ContrastDemo()
    # Function descriptor binds as method.
    method_type = type(ContrastDemo.__dict__["func"]).__name__
    # Slot descriptor is a member descriptor.
    slot_type = type(ContrastDemo.__dict__["slot_val"]).__name__
    # Property descriptor.
    prop_type = type(ContrastDemo.__dict__["prop"]).__name__
    return method_type, slot_type, prop_type


def validating_descriptor_demo() -> tuple[str, str]:
    obj = DescriptorOwner()
    obj.count = 10
    before = obj.count
    try:
        obj.count = -1  # type: ignore[assignment]
        validation = "no-error"
    except ValueError as exc:
        validation = f"value-error:{exc}"
    return str(before), validation  # type: ignore[return-value]
