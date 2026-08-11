"""Callable objects (PY-CAN-CALL-007)."""

from __future__ import annotations

from typing import Any, Callable


class StatefulHandler:
    """Stateful callable passed as a callback."""

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix
        self.calls = 0

    def __call__(self, payload: str, *, suffix: str = "") -> str:
        """Custom signature distinct from construction."""

        self.calls += 1
        return f"{self.prefix}:{payload}{suffix}"

    def reset(self) -> None:
        self.calls = 0


class ToolkitMeta(type):
    """Metaclass whose ``__call__`` intercepts construction."""

    construction_log: list[str] = []

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:  # noqa: N804
        cls.construction_log.append(f"meta:{cls.__name__}")
        instance = super().__call__(*args, **kwargs)
        cls.construction_log.append(f"built:{cls.__name__}")
        return instance


class Parcel(metaclass=ToolkitMeta):
    """Class whose construction goes through the metaclass ``__call__``."""

    def __init__(self, label: str) -> None:
        self.label = label


class InstanceOnlyCallable:
    """``__call__`` placed only on the instance, not on the type."""

    def __init__(self) -> None:
        # Instance attribute shadowing; special lookup ignores instance dict.
        self.__call__ = lambda payload: f"instance:{payload}"  # type: ignore[method-assign]


def use_stateful_callback(handler: Callable[[str], str], payload: str) -> str:
    """Accept a callable object as a callback."""

    return handler(payload)


def class_construction_vs_instance_invocation() -> dict[str, object]:
    """Distinguish class construction from instance invocation."""

    handler = StatefulHandler("parcel")
    construction = handler  # instance is callable
    via_callback = use_stateful_callback(handler, "alpha")
    method = handler.__call__
    return {
        "via_callback": via_callback,
        "call_count": handler.calls,
        "construction_is_instance": construction is handler,
        "method_is_callable": callable(method),
        "direct_call": handler("beta"),
    }


def metaclass_call_interception() -> list[str]:
    """Exercise the metaclass ``__call__`` log."""

    ToolkitMeta.construction_log.clear()
    _ = Parcel("label-a")
    return list(ToolkitMeta.construction_log)


def instance_only_call_does_not_satisfy_special_lookup() -> dict[str, bool]:
    """Instance-only ``__call__`` does not make the instance callable via special lookup."""

    obj = InstanceOnlyCallable()
    return {
        "callable_via_type": callable(obj),
        "has_instance_attr": hasattr(obj, "__call__") and "__call__" in obj.__dict__,
        "type_has_call": hasattr(type(obj), "__call__") and "__call__" in type(obj).__dict__,
    }


def custom_signature_introspection() -> dict[str, object]:
    """Inspect the custom ``__call__`` signature."""

    import inspect

    sig = inspect.signature(StatefulHandler.__call__)
    return {
        "parameters": list(sig.parameters.keys()),
        "text": str(sig),
    }
