"""Module-level attribute interception (PY-CAN-OBJ-008 module-hook distinction)."""

from __future__ import annotations

from typing import Any

# Module-level lazy attribute via PEP 562 __getattr__ and __dir__.
_lazy_store: dict[str, str] = {"dynamic_module_value": "module-dynamic"}


def __getattr__(name: str) -> Any:
    if name in _lazy_store:
        return _lazy_store[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + list(_lazy_store.keys()))


def module_getattr_demo() -> str:
    import record_modeling_kit.module_hook as mh

    # Access via normal attribute lookup triggers module __getattr__.
    return mh.dynamic_module_value  # type: ignore[attr-defined]


def module_getattr_missing_demo() -> str:
    import record_modeling_kit.module_hook as mh

    try:
        _ = mh.missing_module_attr  # type: ignore[attr-defined]
        return "no-error"
    except AttributeError as exc:
        return f"module-missing:{exc}"


def class_vs_module_interception_demo() -> tuple[str, str]:
    # Contrast class-level __getattr__ (ForwardingProxy) with module-level __getattr__.
    from record_modeling_kit.interception import ForwardingProxy, RealTarget

    proxy = ForwardingProxy(RealTarget())
    class_fallback = proxy.dynamic_item  # type: ignore[attr-defined]
    module_fallback = module_getattr_demo()
    return class_fallback, module_fallback
