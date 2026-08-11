"""Registries and decorator-based discovery (PY-CAN-DYN-007)."""

from __future__ import annotations

from typing import Callable

# Decorator registry: object versus string/type key variants.
handler_registry: dict[object, Callable[..., object]] = {}


def register_handler(key: object) -> Callable[[Callable[..., object]], Callable[..., object]]:
    """Decorator that populates handler_registry and returns original or wrapper."""

    def decorator(fn: Callable[..., object]) -> Callable[..., object]:
        # Duplicate-key handling: last write wins (import-order dependency).
        handler_registry[key] = fn
        return fn

    return decorator


# Type-key variant.
type_registry: dict[type, Callable[..., object]] = {}


def register_for_type(tp: type) -> Callable[[Callable[..., object]], Callable[..., object]]:
    def decorator(fn: Callable[..., object]) -> Callable[..., object]:
        type_registry[tp] = fn
        return fn

    return decorator


# String-key variant.
string_registry: dict[str, Callable[..., object]] = {}


def register_for_name(name: str) -> Callable[[Callable[..., object]], Callable[..., object]]:
    def decorator(fn: Callable[..., object]) -> Callable[..., object]:
        string_registry[name] = fn
        return fn

    return decorator


# Decorator replacement/order: wrapping decorator that preserves metadata.
def wrapping_register(key: object) -> Callable[[Callable[..., object]], Callable[..., object]]:
    def decorator(fn: Callable[..., object]) -> Callable[..., object]:
        def wrapper(*args: object, **kwargs: object) -> object:
            return fn(*args, **kwargs)

        wrapper.__name__ = fn.__name__
        wrapper.__wrapped__ = fn  # type: ignore[attr-defined]
        handler_registry[key] = wrapper
        return wrapper

    return decorator


# __init_subclass__ registry across modules.
class PluginBase:
    """Base that auto-registers subclasses via __init_subclass__."""

    registry: dict[str, type] = {}

    def __init_subclass__(cls, *, plugin_name: str | None = None, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        key = plugin_name or cls.__name__
        # Duplicate handling: explicit check could raise, here last wins to show import-order.
        PluginBase.registry[key] = cls


class InvoiceHandler(PluginBase, plugin_name="invoice"):
    pass


class DeliveryHandler(PluginBase, plugin_name="delivery"):
    pass


# Metaclass registry variant.
class HandlerMeta(type):
    registry: dict[str, type] = {}

    def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict[str, object], **kwargs: object) -> type:
        cls = super().__new__(mcs, name, bases, namespace)
        # Skip base itself.
        if name != "RegisteredHandler":
            HandlerMeta.registry[name] = cls
        return cls


class RegisteredHandler(metaclass=HandlerMeta):
    pass


class CatalogHandler(RegisteredHandler):
    pass


class OrderHandler(RegisteredHandler):
    pass


# Consumption helpers.
def dispatch_by_key(key: object, *args: object, **kwargs: object) -> object:
    fn = handler_registry.get(key)
    if fn is None:
        fn = string_registry.get(str(key))  # string/type key fallback
        if fn is None:
            fn = type_registry.get(type(key))  # type key fallback
    if fn is None:
        raise KeyError(f"no handler for {key!r}")
    return fn(*args, **kwargs)


def all_plugins() -> dict[str, type]:
    return dict(PluginBase.registry)


def all_meta_handlers() -> dict[str, type]:
    return dict(HandlerMeta.registry)


# Decorator usage examples (populate registries at import time).
@register_handler("catalog")
def handle_catalog(payload: dict[str, object]) -> str:
    return f"catalog:{payload.get('id')}"


@register_for_type(dict)
def handle_dict(payload: dict) -> str:
    return f"dict-keys:{sorted(payload.keys())!r}"


@register_for_name("order")
def handle_order(payload: object) -> str:
    return f"order:{payload!r}"


# Demonstrate import-order dependency: later import could override.
@register_handler("catalog")
def handle_catalog_override(payload: dict[str, object]) -> str:
    return f"catalog-override:{payload.get('id')}"


class HandlerRegistry:
    """Thin wrapper exposing registry operations."""

    def __init__(self) -> None:
        self._entries: dict[object, Callable[..., object]] = {}

    def register(self, key: object, fn: Callable[..., object]) -> None:
        self._entries[key] = fn

    def resolve(self, key: object) -> Callable[..., object] | None:
        return self._entries.get(key)

    def invoke(self, key: object, *args: object, **kwargs: object) -> object:
        fn = self.resolve(key)
        if fn is None:
            raise KeyError(key)
        return fn(*args, **kwargs)
