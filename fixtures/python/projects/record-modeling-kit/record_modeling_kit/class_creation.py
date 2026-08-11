"""Class creation protocol (PY-CAN-OBJ-001)."""

from __future__ import annotations

from typing import Any

# Base evaluation order is left-to-right; helpers record evaluation.
evaluation_log: list[str] = []


def base_a() -> type:
    evaluation_log.append("base_a")

    class BaseA:
        label = "a"

    return BaseA


def base_b() -> type:
    evaluation_log.append("base_b")

    class BaseB:
        label = "b"

    return BaseB


# __mro_entries__ allows an object used as a base to expand to bases.
class MroEntriesProvider:
    def __mro_entries__(self, orig_bases: tuple[type, ...]) -> tuple[type, ...]:
        class Provided:
            provided = True

        return (Provided,)


mro_provider = MroEntriesProvider()


# Custom namespace returned by __prepare__.
class CustomNamespace(dict):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self["prepared_marker"] = "from-prepare"


class PrepareMeta(type):
    @classmethod
    def __prepare__(
        metacls,
        name: str,
        bases: tuple[type, ...],
        **kwargs: Any,
    ) -> dict[str, Any]:
        ns: dict[str, Any] = CustomNamespace()
        ns["prepare_seen_kwargs"] = dict(kwargs)
        return ns

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> type:
        # Capture class keywords passed at definition site.
        namespace["_class_keywords"] = dict(kwargs)
        # Body order: attributes defined sequentially retain order.
        namespace["_creation_order"] = [k for k in namespace if not k.startswith("_")]
        return super().__new__(mcs, name, bases, namespace)


# Class decoration; one decorator wraps, one replaces.
def add_tag(cls: type) -> type:
    cls.tagged = True  # type: ignore[attr-defined]
    return cls


def replace_with_proxy(cls: type) -> type:
    class Proxy:
        original = cls
        replaced = True

    return Proxy  # type: ignore[return-value]


# Demonstrates base evaluation, MRO entries, metaclass selection, __prepare__,
# body order, creation, and decoration.
@add_tag
class BaseMarker(metaclass=PrepareMeta, debug=True):
    first = 1
    second = 2
    computed = first + second


# Second class using MRO entries and keyword arguments.
class DerivedWithMro(mro_provider, metaclass=PrepareMeta, audit=True):
    extra = "derived"


# Replacement decorator variant (PY-CAN-OBJ-001 replacement decorator).
@replace_with_proxy
class ReplacementDecoratorDemo:
    value = 42


# Metaclass conflict demonstration (valid source catches the failure).
class MetaA(type):
    pass


class MetaB(type):
    pass


class BaseWithMetaA(metaclass=MetaA):
    pass


class BaseWithMetaB(metaclass=MetaB):
    pass


def metaclass_conflict_demo() -> str:
    try:
        class Conflict(BaseWithMetaA, BaseWithMetaB):  # type: ignore[misc]
            pass

        return "no-error"
    except TypeError as exc:
        return f"metaclass-conflict:{exc}"


def evaluated_bases() -> list[str]:
    evaluation_log.clear()
    # Trigger evaluation in class statement; bases are call results.
    class EvalDemo(base_a(), base_b()):
        pass

    _ = EvalDemo
    return list(evaluation_log)


def mro_entries_demo() -> tuple[str, ...]:
    return tuple(c.__name__ for c in DerivedWithMro.__mro__)


def custom_namespace_demo() -> dict[str, Any]:
    return dict(BaseMarker.__dict__.get("_class_keywords", {}))


def class_decorator_replacement_demo() -> bool:
    return bool(getattr(ReplacementDecoratorDemo, "replaced", False))
