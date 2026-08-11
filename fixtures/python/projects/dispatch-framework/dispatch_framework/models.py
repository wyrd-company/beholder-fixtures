"""Declarative descriptor models (PY-CAN-DYN-012)."""

from __future__ import annotations

from typing import Any


class Field:
    """Descriptor for typed field; class versus instance access type differs."""

    def __init__(self, field_type: type, *, default: Any = None) -> None:
        self.field_type = field_type
        self.default = default
        self.name: str | None = None
        self.private_name: str | None = None

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, instance: Any, owner: type | None = None) -> Any:
        if instance is None:
            # Class access returns descriptor itself (different type than instance access).
            return self
        return getattr(instance, self.private_name or f"_{self.name}", self.default)

    def __set__(self, instance: Any, value: Any) -> None:
        if value is not None and not isinstance(value, self.field_type):
            raise TypeError(f"{self.name} expects {self.field_type.__name__}")
        setattr(instance, self.private_name or f"_{self.name}", value)


class Relationship:
    """String relationship that injects reverse attribute on target."""

    def __init__(self, target_name: str, *, backref: str | None = None) -> None:
        self.target_name = target_name  # string reference, resolved lazily
        self.backref = backref
        self.name: str | None = None

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: Any, owner: type | None = None) -> Any:
        if instance is None:
            return self
        return getattr(instance, f"_{self.name}", None)

    def __set__(self, instance: Any, value: Any) -> None:
        setattr(instance, f"_{self.name}", value)
        if value is not None and self.backref:
            # Injected reverse attribute.
            setattr(value, self.backref, instance)


# Registry setup variant: model registry populated via __init_subclass__ / metaclass.


class ModelMeta(type):
    registry: dict[str, type] = {}

    def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any], **kw: Any) -> type:
        cls = super().__new__(mcs, name, bases, dict(namespace))
        if name != "Model":
            ModelMeta.registry[name] = cls
            # Generated attributes: collect Field names.
            fields = {k: v for k, v in namespace.items() if isinstance(v, Field)}
            cls._fields = fields  # type: ignore[attr-defined]
            rels = {k: v for k, v in namespace.items() if isinstance(v, Relationship)}
            cls._relationships = rels  # type: ignore[attr-defined]
        return cls


class Model(metaclass=ModelMeta):
    _fields: dict[str, Field] = {}
    _relationships: dict[str, Relationship] = {}

    def __init__(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in self._fields}


# Concrete models using string relationships.
class CatalogOwner(Model):
    name = Field(str, default="")
    region = Field(str, default="default")


class CatalogRecord(Model):
    title = Field(str, default="")
    count = Field(int, default=0)
    owner = Relationship("CatalogOwner", backref="record")


# Checker-plugin / static mismatch note: string target "CatalogOwner" resolves at runtime
# but a static checker without plugin would see it as unresolved; runtime handles it via registry.
def resolve_relationship_target(rel: Relationship) -> type | None:
    return ModelMeta.registry.get(rel.target_name)
