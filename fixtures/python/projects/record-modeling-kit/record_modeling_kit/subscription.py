"""Class subscription (PY-CAN-OBJ-018)."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

T = TypeVar("T")


class SubscribableMeta(type):
    """Metaclass __getitem__ has precedence over class __class_getitem__ when accessed via class."""

    def __getitem__(cls, key: Any) -> str:
        return f"meta-getitem:{key!r}"


class SubscribableModel(metaclass=SubscribableMeta):
    """Contrast __class_getitem__, metaclass __getitem__, and instance __getitem__."""

    # Class subscription for typing / generic alias.
    @classmethod
    def __class_getitem__(cls, key: Any) -> str:
        return f"class-getitem:{key!r}"

    def __getitem__(self, key: Any) -> str:
        return f"instance-getitem:{key!r}"

    # Non-typing use: registry lookup.
    registry: dict[str, str] = {"a": "alpha"}


class WithClassGetItem:
    @classmethod
    def __class_getitem__(cls, key: Any) -> str:
        if isinstance(key, tuple):
            return f"tuple-key:{key}"
        if isinstance(key, slice):
            return f"slice:{key.start}:{key.stop}"
        return f"key:{key}"


class BuiltinGenericDemo:
    # Built-in generic alias: list[int] is valid syntax, not calling our code.
    data: list[int] = [1, 2]


def metaclass_precedence_demo() -> tuple[str, str]:
    # Access via class uses metaclass __getitem__ ahead of __class_getitem__.
    via_class = SubscribableModel["x"]  # metaclass wins
    # Direct call to __class_getitem__ bypasses metaclass dispatch.
    via_class_getitem = SubscribableModel.__class_getitem__("y")
    return via_class, via_class_getitem


def instance_getitem_demo() -> str:
    obj = SubscribableModel()
    return obj["instance-key"]


def tuple_slice_key_demo() -> tuple[str, str]:
    a = WithClassGetItem[(1, 2)]
    b = WithClassGetItem[1:3]
    return a, b


def builtin_generic_alias_demo() -> str:
    # Built-in generic alias form.
    alias = list[int]
    return f"builtin-alias:{alias}"


def nontyping_use_demo() -> str:
    # Non-typing subscription used as registry/lookup.
    value = SubscribableModel.registry["a"]
    return f"registry-lookup:{value}"
