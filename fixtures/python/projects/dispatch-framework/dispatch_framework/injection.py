"""Annotation/signature-driven runtime models and dependency injection (PY-CAN-DYN-008)."""

from __future__ import annotations

import inspect
from typing import Annotated, get_args, get_origin, get_type_hints

# Field specifier for dataclass_transform contract (runtime drift example).
try:
    from dispatch_framework.models import Field as _ModelField
except Exception:
    _ModelField = object  # fallback for import order during static analysis
Field = _ModelField  # type: ignore[assignment]

# Minimal container: providers keyed by type, with scope and cycle detection.


class Container:
    def __init__(self) -> None:
        self._providers: dict[type, object] = {}
        self._singletons: dict[type, object] = {}
        self._resolving: set[type] = set()

    def register(self, tp: type, provider: object, *, singleton: bool = False) -> None:
        # Duplicate/ambiguity: last wins; caller can inspect.
        self._providers[tp] = (provider, singleton)

    def _resolve_single(self, tp: type) -> object:
        if tp in self._singletons:
            return self._singletons[tp]
        if tp in self._resolving:
            raise RuntimeError(f"provider cycle detected for {tp!r}")
        entry = self._providers.get(tp)
        if entry is None:
            raise KeyError(f"no provider for {tp!r}")
        provider, singleton = entry
        self._resolving.add(tp)
        try:
            if callable(provider):
                sig = inspect.signature(provider)
                kwargs: dict[str, object] = {}
                # Inspect annotations/defaults and resolve dependencies recursively.
                hints = {}
                try:
                    hints = get_type_hints(provider)
                except Exception:
                    hints = getattr(provider, "__annotations__", {})
                for name, param in sig.parameters.items():
                    ann = hints.get(name, param.annotation)
                    origin = get_origin(ann)
                    # Annotated unwrapping.
                    if origin is Annotated:
                        ann = get_args(ann)[0]
                    if ann is not inspect.Parameter.empty and ann in self._providers:
                        kwargs[name] = self._resolve_single(ann)
                    elif param.default is not inspect.Parameter.empty:
                        kwargs[name] = param.default
                    else:
                        # No provider, try default injection or fail.
                        kwargs[name] = None
                instance = provider(**kwargs)
            else:
                instance = provider
        finally:
            self._resolving.remove(tp)
        if singleton:
            self._singletons[tp] = instance
        return instance

    def resolve(self, tp: type) -> object:
        return self._resolve_single(tp)

    def call(self, fn: object, **extra: object) -> object:
        """Call fn injecting annotated parameters from providers."""
        sig = inspect.signature(fn)  # wrapper loses signature if not preserved
        hints = {}
        try:
            hints = get_type_hints(fn)
        except Exception:
            hints = getattr(fn, "__annotations__", {})
        bound: dict[str, object] = {}
        for name, param in sig.parameters.items():
            if name in extra:
                bound[name] = extra[name]
                continue
            ann = hints.get(name, param.annotation)
            origin = get_origin(ann)
            if origin is Annotated:
                ann = get_args(ann)[0]
            if ann is not inspect.Parameter.empty and ann in self._providers:
                bound[name] = self._resolve_single(ann)  # type: ignore[arg-type]
            elif param.default is not inspect.Parameter.empty:
                bound[name] = param.default
            else:
                bound[name] = None
        return fn(**bound)  # type: ignore[operator]


# Postponed-hint resolution variant: string annotations need get_type_hints.
class ServiceA:
    value: str = "A"


class ServiceB:
    def __init__(self, dep: "ServiceA") -> None:  # postponed string annotation
        self.dep = dep


def build_model(container: Container) -> ServiceB:
    # Register provider that needs postponed resolution.
    container.register(ServiceA, ServiceA, singleton=True)

    def _make_b(dep: ServiceA) -> ServiceB:
        return ServiceB(dep)

    container.register(ServiceB, _make_b)
    return container.resolve(ServiceB)  # type: ignore[return-value]


# Annotated variant with metadata.
class ConfigValue:
    def __init__(self, raw: Annotated[str, "config-key:region"]) -> None:
        self.raw = raw


# Wrapper loses signature variant versus preserved.
import functools


def wrapper_loses_signature(fn):  # type: ignore[no-untyped-def]
    def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
        return fn(*args, **kwargs)

    return wrapper


def wrapper_preserves_signature(fn):  # type: ignore[no-untyped-def]
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
        return fn(*args, **kwargs)

    return wrapper


@wrapper_loses_signature
def handler_without_wraps(item: ServiceA, count: int = 2) -> str:
    return f"{item.value}:{count}"


@wrapper_preserves_signature
def handler_with_wraps(item: ServiceA, count: int = 2) -> str:
    return f"{item.value}:{count}"


def injected_call(container: Container, fn: object) -> object:
    return container.call(fn)


# Provider cycle / ambiguity / scope variants.
def cycle_demo() -> str:
    c = Container()

    class NodeA:
        pass

    class NodeB:
        pass

    # Cycle: A depends on B, B depends on A.
    def make_a(b: NodeB) -> NodeA:  # type: ignore
        return NodeA()

    def make_b(a: NodeA) -> NodeB:  # type: ignore
        return NodeB()

    # With postponed evaluation, local annotations are stringified; restore real types
    # so the container can detect the cycle.
    make_a.__annotations__ = {"b": NodeB, "return": NodeA}
    make_b.__annotations__ = {"a": NodeA, "return": NodeB}

    c.register(NodeA, make_a)
    c.register(NodeB, make_b)
    try:
        c.resolve(NodeA)
        return "no-cycle"
    except RuntimeError as exc:
        return str(exc)


# Static transform contract and runtime drift variant.
try:
    from typing import dataclass_transform  # type: ignore[attr-defined]
except ImportError:
    from typing_extensions import dataclass_transform  # type: ignore[no-redef, import-not-found]


@dataclass_transform(field_specifiers=(Field,))  # type: ignore[name-defined]
def define_catalog_model(name: str, *, title: Field, count: Field) -> type:  # type: ignore[no-untyped-def]
    # Static checker treats this as a dataclass-like factory generating __init__(title, count).
    # Runtime shape is built via ModelMeta registry, not dataclass fields, demonstrating drift.
    from dispatch_framework.models import CatalogRecord

    return CatalogRecord


def static_transform_runtime_drift_demo() -> tuple[str, list[str], list[str]]:
    # Static transform expects __init__ with title/count from decorator contract.
    # Runtime drift: actual CatalogRecord fields come from ModelMeta._fields, not dataclass.
    from dispatch_framework.models import CatalogRecord as CR

    static_params = ["title", "count"]
    runtime_fields = sorted(CR._fields.keys())
    drift = "match" if static_params == runtime_fields else "drift:static-vs-runtime"
    return drift, static_params, runtime_fields


# Static transform / runtime drift comment: runtime inspects real hints, static checker may differ.
def drift_example(value: "ServiceA | None" = None) -> str:  # postponed union
    hints = get_type_hints(drift_example)
    return str(hints.get("value"))
