"""Subclass and descriptor initialization hooks (PY-CAN-OBJ-011)."""

from __future__ import annotations

from typing import Any


# Registry via __init_subclass__.
class RegisteredModel:
    registry: dict[str, type] = {}

    def __init_subclass__(cls, kind: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if kind is not None:
            if kind in RegisteredModel.registry:
                raise ValueError(f"duplicate kind {kind!r}")
            RegisteredModel.registry[kind] = cls
            cls.kind = kind  # type: ignore[attr-defined]

    def __init__(self, value: str) -> None:
        self.value = value


class AlphaRecord(RegisteredModel, kind="alpha"):
    pass


class BetaRecord(RegisteredModel, kind="beta"):
    pass


# Cooperative multiple bases with __init_subclass__.
class MixinA:
    def __init_subclass__(cls, tag_a: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if tag_a is not None:
            cls.tag_a = tag_a  # type: ignore[attr-defined]


class MixinB:
    def __init_subclass__(cls, tag_b: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if tag_b is not None:
            cls.tag_b = tag_b  # type: ignore[attr-defined]


class CooperativeModel(MixinA, MixinB):
    pass


class CooperativeWithKind(MixinA, MixinB, RegisteredModel, tag_a="a", tag_b="b", kind="coop"):  # type: ignore[call-arg]
    pass


# __set_name__ descriptor.
class TaggedDescriptor:
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.private = f"_{name}_tagged"

    def __get__(self, instance: object | None, owner: type | None = None) -> Any:
        if instance is None:
            return self
        return instance.__dict__.get(self.private, f"default:{self.name}")

    def __set__(self, instance: object, value: Any) -> None:
        instance.__dict__[self.private] = value


class TaggedOwner:
    label = TaggedDescriptor()
    count = TaggedDescriptor()


def unknown_keyword_demo() -> str:
    try:
        class Bad(RegisteredModel, unknown="oops"):  # type: ignore[call-arg]
            pass

        _ = Bad
        return "no-error"
    except TypeError as exc:
        return f"unknown-keyword:{exc}"


def cooperative_bases_demo() -> tuple[str, str, str]:
    # CooperativeWithKind inherits cooperatively from MixinA+MixinB+RegisteredModel.
    return (
        getattr(CooperativeWithKind, "tag_a", "no-a"),  # type: ignore[attr-defined]
        getattr(CooperativeWithKind, "tag_b", "no-b"),  # type: ignore[attr-defined]
        getattr(CooperativeWithKind, "kind", "no-kind"),  # type: ignore[attr-defined]
    )


def set_name_demo() -> tuple[str, str]:
    return TaggedOwner.label.name, TaggedOwner.count.name  # type: ignore[attr-defined]


def descriptor_attached_later_demo() -> tuple[bool, str]:
    """Descriptor attached after class creation does not get __set_name__ automatically."""

    class Late:
        pass

    desc = TaggedDescriptor()
    Late.late_field = desc  # type: ignore[attr-defined]
    has_name = hasattr(desc, "name")
    # Manual rebind would be needed; show that late assignment lacks name.
    # Workaround: call __set_name__ manually if desired.
    if not has_name:
        desc.__set_name__(Late, "late_field")
        after = desc.name  # type: ignore[attr-defined]
        return False, after
    return True, desc.name  # type: ignore[attr-defined]


def metaclass_duplication_demo() -> str:
    # Metaclass __new__ and __init_subclass__ both observe creation.
    events: list[str] = []

    class TrackingMeta(type):
        def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any], **kwargs: Any) -> type:
            events.append(f"meta-new:{name}")
            return super().__new__(mcs, name, bases, namespace)

    class BaseWithMeta(metaclass=TrackingMeta):
        def __init_subclass__(cls, **kwargs: Any) -> None:
            events.append(f"init-subclass:{cls.__name__}")
            super().__init_subclass__(**kwargs)

    class Child(BaseWithMeta):
        pass

    _ = Child
    return ",".join(events)
