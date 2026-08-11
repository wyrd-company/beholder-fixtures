"""Class-body namespace boundary (PY-CAN-BIND-004)."""

from __future__ import annotations

from typing import ClassVar


class PreparedNamespaceMeta(type):
    """Metaclass that prepares a namespace before class body execution."""

    @classmethod
    def __prepare__(
        metacls,
        name: str,
        bases: tuple[type, ...],
        **kwargs: object,
    ) -> dict[str, object]:
        prepared: dict[str, object] = {"prepared_marker": "metaclass-prepared"}
        return prepared

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, object],
        **kwargs: object,
    ) -> type:
        namespace["class_body_marker"] = "class-body-added"
        return super().__new__(mcs, name, bases, namespace)


class SettingsProfile(metaclass=PreparedNamespaceMeta):
    """Compute class attributes and expose method lookup boundaries."""

    region: ClassVar[str] = "default-region"
    tier = "standard"

    class_body_local = "class-local"
    computed = class_body_local.upper()

    def resolve(self) -> str:
        return f"{self.region}:{self.tier}:{self.computed}"

    @classmethod
    def class_dict_lookup(cls) -> str:
        return cls.__dict__["computed"]


def method_lexical_boundary() -> str:
    """Show a method bare name resolves past a class-body binding."""

    tier = "enclosing-tier"

    class BoundaryProfile:
        tier = "class-tier"

        def bare_tier(self) -> str:
            return tier

    return BoundaryProfile().bare_tier()


class TypeScopedRegistry[T]:
    """Exercise type-parameter scope introduced in Python 3.12."""

    store: dict[str, T]

    def __init__(self) -> None:
        self.store = {}

    def put(self, key: str, value: T) -> None:
        self.store[key] = value

    def get(self, key: str) -> T | None:
        return self.store.get(key)


def class_comprehension_edge() -> list[str]:
    """Use a comprehension whose iterable is bound only in the class body."""

    class ComprehensionEdge:
        seeds = ("alpha", "beta")
        labels = [seed.upper() for seed in seeds]

    return ComprehensionEdge.labels


def nested_class_expression() -> str:
    """Reference `__class__` from a nested scope inside a method."""

    class Outer:
        label = "outer-label"

        def build(self) -> str:
            def inner() -> str:
                return __class__.label  # noqa: F821

            return inner()

    return Outer().build()
