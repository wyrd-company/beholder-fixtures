"""Dynamic and local class creation (PY-CAN-OBJ-020)."""

from __future__ import annotations

import pickle
from typing import Any


# Dynamic class via type().
def build_dynamic_type(name: str, value: int) -> type:
    def method(self) -> str:
        return f"{self.label}:{value}"

    # Class body absent from source; supplied as dict.
    cls = type(name, (object,), {"label": name.lower(), "action": method, "__module__": __name__})
    return cls


DynamicRecord = build_dynamic_type("DynamicRecord", 7)


# Local class inside function with closure capture.
def make_local_class(prefix: str) -> type:
    captured = prefix.upper()

    class LocalRecord:
        kind = captured
        prefix_value = prefix

        def greet(self) -> str:
            return f"{self.kind}:{self.prefix_value}"

        def __repr__(self) -> str:
            return f"LocalRecord({self.kind})"

    return LocalRecord


# Stable factory/registry that caches generated classes.
class Registry:
    _cache: dict[str, type] = {}

    @classmethod
    def get(cls, name: str) -> type:
        if name not in cls._cache:
            generated = type(name, (object,), {"registry_name": name, "__module__": __name__})
            cls._cache[name] = generated
        return cls._cache[name]


def closure_capture_demo() -> tuple[str, str]:
    LocalA = make_local_class("alpha")
    LocalB = make_local_class("beta")
    return LocalA().greet(), LocalB().greet()


def qualified_name_and_pickle_demo() -> tuple[str, bool]:
    Local = make_local_class("pickle")
    obj = Local()
    obj.value = 123  # type: ignore[attr-defined]
    # Qualified name includes function <locals>.
    qname = Local.__qualname__
    # For local classes, pickling by default fails unless we handle it; demonstrate qualified name.
    try:
        data = pickle.dumps(obj)
        restored = pickle.loads(data)
        pickled = isinstance(restored, Local)
    except Exception as exc:
        # Expected: local class may not pickle without registry.
        pickled = False
        qname = f"{qname}:pickle-error:{type(exc).__name__}"
    return qname, pickled


def synthetic_methods_demo() -> str:
    cls = build_dynamic_type("Synthetic", 99)
    # Add synthetic method after creation.
    def extra(self) -> str:
        return f"extra:{self.label}"

    cls.extra = extra  # type: ignore[attr-defined]
    obj = cls()
    return obj.extra()  # type: ignore[attr-defined]


def factory_registry_demo() -> bool:
    a1 = Registry.get("ItemA")
    a2 = Registry.get("ItemA")
    b = Registry.get("ItemB")
    return (a1 is a2) and (a1 is not b)


def type_creation_demo() -> str:
    cls = type("ViaType", (object,), {"x": 1, "y": 2})
    obj = cls()
    return f"{obj.x},{obj.y}"


# Ensure class body absent case is documented.
def class_body_absent_note() -> str:
    return "type()-created classes have no class body in source text"
