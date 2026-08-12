"""Annotation/signature-driven runtime models and dependency injection (PY-CAN-DYN-008)."""

from __future__ import annotations

import inspect
from typing import Annotated, dataclass_transform, get_args, get_origin, get_type_hints

from dispatch_framework.models import Field

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


# Static-transform contract and runtime-drift variant (PEP 681).
# The marker is applied to a real base class: a static type checker synthesizes a
# dataclass-style __init__ from each subclass's Field specifiers. At runtime the
# base provides a permissive __init__ that accepts any keyword, so the runtime
# shape drifts from the statically declared field set.
@dataclass_transform(field_specifiers=(Field,))
class TransformedModel:
    """Base treated as dataclass-like by a checker, permissive at runtime."""

    def __init__(self, **kwargs: object) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)


class CatalogInput(TransformedModel):
    # A checker synthesizes __init__(self, *, title: str = ..., count: int = ...)
    # from these Field specifiers; the runtime __init__ ignores that contract.
    title: str = Field(str, default="")
    count: int = Field(int, default=0)


def static_transform_runtime_drift_demo() -> tuple[str, list[str], list[str]]:
    """Contrast the synthesized static __init__ with permissive runtime construction.

    A checker's synthesized ``CatalogInput.__init__`` declares only ``title`` and
    ``count`` from the Field specifiers. At runtime the permissive base
    ``__init__`` also accepts a keyword the static contract forbids, so the
    instance carries a field the checker never declared — genuine
    static-versus-runtime drift.
    """
    static_fields = sorted(
        name for name, value in vars(CatalogInput).items() if isinstance(value, Field)
    )
    instance = CatalogInput(title="widget", count=3, note="runtime-only")
    runtime_only = sorted(k for k in vars(instance) if not k.startswith("_"))
    drift = "drift:static-vs-runtime" if runtime_only else "match"
    return drift, static_fields, runtime_only


# Static transform / runtime drift comment: runtime inspects real hints, static checker may differ.
def drift_example(value: "ServiceA | None" = None) -> str:  # postponed union
    hints = get_type_hints(drift_example)
    return str(hints.get("value"))
