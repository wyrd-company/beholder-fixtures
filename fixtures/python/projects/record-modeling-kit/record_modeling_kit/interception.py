"""Attribute interception (PY-CAN-OBJ-008)."""

from __future__ import annotations

from typing import Any


class AttributeLog:
    def __init__(self) -> None:
        self.log: list[str] = []


class ForwardingProxy:
    """Safe forwarding through __getattribute__, __getattr__, __setattr__, __delattr__."""

    def __init__(self, target: Any) -> None:
        # Use object.__setattr__ to avoid recursion.
        object.__setattr__(self, "_target", target)
        object.__setattr__(self, "log", AttributeLog().log)

    def __getattribute__(self, name: str) -> Any:
        # Avoid infinite recursion: fetch via object.__getattribute__.
        if name in ("_target", "log", "__class__", "__dict__"):
            return object.__getattribute__(self, name)
        target = object.__getattribute__(self, "_target")
        log: list[str] = object.__getattribute__(self, "log")
        log.append(f"getattribute:{name}")
        try:
            return getattr(target, name)
        except AttributeError:
            # Fallback will be attempted via __getattr__.
            raise

    def __getattr__(self, name: str) -> Any:
        # Fallback for missing attributes.
        log: list[str] = object.__getattribute__(self, "log")
        log.append(f"getattr:{name}")
        if name.startswith("dynamic_"):
            return f"dynamic:{name}"
        raise AttributeError(f"{name} not found via proxy")

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ("_target", "log"):
            object.__setattr__(self, name, value)
            return
        log: list[str] = object.__getattribute__(self, "log")
        log.append(f"setattr:{name}={value!r}")
        setattr(object.__getattribute__(self, "_target"), name, value)

    def __delattr__(self, name: str) -> None:
        if name in ("_target", "log"):
            object.__delattr__(self, name)
            return
        log: list[str] = object.__getattribute__(self, "log")
        log.append(f"delattr:{name}")
        delattr(object.__getattribute__(self, "_target"), name)


class RealTarget:
    def __init__(self) -> None:
        self.existing = "present"
        self.count = 1


def safe_forwarding_demo() -> tuple[str, str, list[str]]:
    target = RealTarget()
    proxy = ForwardingProxy(target)
    existing = proxy.existing  # via __getattribute__
    dynamic = proxy.dynamic_item  # type: ignore[attr-defined]  # via __getattr__
    return existing, dynamic, list(proxy.log)  # type: ignore[attr-defined]


def recursion_failure_demo() -> str:
    class Broken:
        def __getattribute__(self, name: str) -> Any:
            # Forgetting to use object.__getattribute__ causes recursion on __dict__ lookup.
            return self.__dict__[name]  # type: ignore[attr-defined]

    obj = Broken()
    # Use object.__setattr__-style bypass to avoid triggering __getattribute__ while seeding.
    object.__setattr__(obj, "value", "ok")
    try:
        _ = obj.value
        return "no-error"
    except RecursionError as exc:
        return f"recursion:{type(exc).__name__}"
    except KeyError as exc:
        return f"key-error:{exc}"


def special_method_bypass_demo() -> tuple[int, str]:
    class Special:
        def __len__(self) -> int:
            return 3

    obj = Special()
    # Instance attribute does not affect special lookup.
    obj.__dict__["__len__"] = lambda: 99  # type: ignore[attr-defined]
    via_len = len(obj)
    via_getattr = obj.__dict__["__len__"]()  # type: ignore[attr-defined]
    return via_len, str(via_getattr)


def set_delete_demo() -> tuple[str, str]:
    target = RealTarget()
    proxy = ForwardingProxy(target)
    proxy.new_attr = "added"  # type: ignore[attr-defined]
    added = target.new_attr  # type: ignore[attr-defined]
    del proxy.new_attr  # type: ignore[attr-defined]
    missing = hasattr(target, "new_attr")
    return added, str(missing)


def proxy_target_failure_demo() -> str:
    target = RealTarget()
    proxy = ForwardingProxy(target)
    try:
        _ = proxy.missing_without_dynamic  # type: ignore[attr-defined]
        return "no-error"
    except AttributeError as exc:
        return f"proxy-missing:{exc}"
