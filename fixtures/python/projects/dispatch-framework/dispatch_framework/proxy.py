"""Proxies and transparent delegation (PY-CAN-DYN-009)."""

from __future__ import annotations

import copy
import functools
import pickle
import weakref
from typing import Any


class Proxy:
    """Transparent proxy forwarding ordinary attributes and explicit protocols."""

    def __init__(self, target: Any) -> None:
        object.__setattr__(self, "_target", target)

    # Ordinary attribute forwarding.
    def __getattr__(self, name: str) -> Any:
        return getattr(object.__getattribute__(self, "_target"), name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_target":
            object.__setattr__(self, name, value)
        else:
            setattr(object.__getattribute__(self, "_target"), name, value)

    def __delattr__(self, name: str) -> None:
        if name == "_target":
            object.__delattr__(self, name)
        else:
            delattr(object.__getattribute__(self, "_target"), name)

    # Explicit forwarding: call.
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        target = object.__getattribute__(self, "_target")
        return target(*args, **kwargs)

    # Iteration / context / operators: must be defined on type, not via __getattr__.
    def __iter__(self):  # type: ignore[no-untyped-def]
        return iter(object.__getattribute__(self, "_target"))

    def __next__(self):  # type: ignore[no-untyped-def]
        return next(object.__getattribute__(self, "_target"))

    def __enter__(self):  # type: ignore[no-untyped-def]
        target = object.__getattribute__(self, "_target")
        if hasattr(target, "__enter__"):
            return target.__enter__()
        return self

    def __exit__(self, *exc):  # type: ignore[no-untyped-def]
        target = object.__getattribute__(self, "_target")
        if hasattr(target, "__exit__"):
            return target.__exit__(*exc)
        return False

    def __len__(self) -> int:
        return len(object.__getattribute__(self, "_target"))

    def __bool__(self) -> bool:
        return bool(object.__getattribute__(self, "_target"))

    def __getitem__(self, key: Any) -> Any:
        return object.__getattribute__(self, "_target")[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        object.__getattribute__(self, "_target")[key] = value

    def __contains__(self, item: Any) -> bool:
        return item in object.__getattribute__(self, "_target")

    def __add__(self, other: Any) -> Any:
        return object.__getattribute__(self, "_target") + other

    def __radd__(self, other: Any) -> Any:
        return other + object.__getattribute__(self, "_target")

    # Special methods need type-level definitions: __getattr__ alone would not cover them.
    def __str__(self) -> str:
        return str(object.__getattribute__(self, "_target"))

    def __repr__(self) -> str:
        return f"Proxy({object.__getattribute__(self, '_target')!r})"

    # Identity, instance checks, pickling, descriptors, weakrefs expose proxy.
    def unwrap(self) -> Any:
        return object.__getattribute__(self, "_target")


def identity_exposes_proxy() -> tuple[bool, bool]:
    target: list[int] = [1, 2]
    proxy = Proxy(target)
    same_identity = proxy is target
    isinstance_proxy = isinstance(proxy, list)
    return same_identity, isinstance_proxy


def pickle_exposes_proxy() -> tuple[bool, str]:
    target = {"key": "value"}
    proxy = Proxy(target)
    data = pickle.dumps(proxy)
    restored = pickle.loads(data)
    # Restored is a Proxy wrapping a dict; identity differs.
    return isinstance(restored, Proxy), type(restored.unwrap()).__name__


class DescriptorTarget:
    val = 7

    @property
    def computed(self) -> int:
        return self.val * 2


def descriptor_exposes_proxy() -> int:
    target = DescriptorTarget()
    proxy = Proxy(target)
    # Descriptor binding still works through proxy via __getattr__.
    return proxy.computed  # type: ignore[no-any-return]


def weakref_exposes_proxy() -> str:
    class Payload:
        pass

    target = Payload()
    proxy = Proxy(target)
    try:
        weakref.ref(proxy)
        weak_kind = "proxy-weakref"
    except TypeError:
        weak_kind = "no-weakref"
    # Direct weakref to target succeeds; proxy may or may not be weak-referenceable.
    ref = weakref.ref(target)
    return f"{weak_kind}:{ref() is target}"


# Wrapper metadata only aids introspection (functools.wraps / update_wrapper).
def traced_proxy(target: Any) -> Any:
    @functools.wraps(target)  # type: ignore[arg-type]
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return target(*args, **kwargs)

    wrapper.__wrapped__ = target  # type: ignore[attr-defined]
    return wrapper
