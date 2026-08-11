"""True dangling attributes versus dynamic provision (PY-CAN-DIAG-021).

Places an actual missing attribute beside equivalent-looking
module/class/proxy dynamic cases.
"""

from __future__ import annotations

import types
from typing import Any


# ---------------------------------------------------------------------------
# True dangling attribute
# ---------------------------------------------------------------------------


class TrueDangling:
    """Class with a genuinely missing attribute."""

    existing = 123


def demo_true_dangling() -> dict[str, object]:
    """True missing attribute raises AttributeError and hasattr is False."""

    obj = TrueDangling()
    try:
        _ = obj.missing_xyz  # type: ignore[attr-defined]
        raised = False
        msg = ""
    except AttributeError as exc:
        raised = True
        msg = str(exc)
    return {
        "raised": raised,
        "hasattr": hasattr(obj, "missing_xyz"),
        "getattr_default": getattr(obj, "missing_xyz", "default"),
        "msg": msg,
    }


# ---------------------------------------------------------------------------
# Dynamic provision via module __getattr__ (PEP 562)
# ---------------------------------------------------------------------------

dynamic_module = types.ModuleType("diagnostics_toolkit.dynamic_module_demo")


def _module_getattr(name: str) -> Any:
    if name.startswith("dynamic_"):
        return f"dynamic-module:{name}"
    raise AttributeError(f"module {dynamic_module.__name__!r} has no attribute {name!r}")


def _module_dir() -> list[str]:
    return ["existing_module_attr", "dynamic_foo", "dynamic_bar"]


dynamic_module.__getattr__ = _module_getattr  # type: ignore[attr-defined]
dynamic_module.__dir__ = _module_dir  # type: ignore[attr-defined]
dynamic_module.existing_module_attr = "present"  # type: ignore[attr-defined]


def demo_module_dynamic() -> dict[str, object]:
    """Module provides attribute dynamically via __getattr__."""

    # Simulate module-like access via the module object.
    try:
        val = dynamic_module.dynamic_foo  # type: ignore[attr-defined]
        missing_raises = False
    except AttributeError:
        val = None
        missing_raises = True
    missing_via_hasattr = hasattr(dynamic_module, "dynamic_foo")
    missing_via_nonexistent = False
    try:
        _ = dynamic_module.nonexistent_xyz  # type: ignore[attr-defined]
    except AttributeError:
        missing_via_nonexistent = True
    return {
        "dynamic_value": val,
        "hasattr_dynamic": missing_via_hasattr,
        "missing_raises": missing_via_nonexistent,
        "missing_via_hasattr_false": not hasattr(dynamic_module, "nonexistent_xyz"),
        "getattr_default": getattr(dynamic_module, "dynamic_foo", None),
    }


# ---------------------------------------------------------------------------
# Dynamic provision via class __getattr__ and proxy
# ---------------------------------------------------------------------------


class WithClassGetattr:
    """Class that provides dynamic attributes via __getattr__."""

    def __getattr__(self, name: str) -> str:
        if name.startswith("dynamic_"):
            return f"dynamic-class:{name}"
        raise AttributeError(f"{type(self).__name__!r} has no attribute {name!r}")

    existing_class_attr = "present"


class ForwardingProxy:
    """Proxy that forwards dynamic names to a target."""

    def __init__(self, target: Any) -> None:
        self._target = target

    def __getattr__(self, name: str) -> Any:
        if name.startswith("dynamic_"):
            return f"proxy-dynamic:{name}"
        # Fallback to target if it has the attribute
        try:
            return getattr(self._target, name)
        except AttributeError as exc:
            raise AttributeError(f"proxy has no attribute {name!r}") from exc


def demo_class_dynamic() -> dict[str, object]:
    """Class instance provides attribute dynamically."""

    obj = WithClassGetattr()
    dynamic_val = obj.dynamic_bar  # type: ignore[attr-defined]
    hasattr_dynamic = hasattr(obj, "dynamic_bar")
    try:
        _ = obj.nonexistent_xyz  # type: ignore[attr-defined]
        missing_raises = False
    except AttributeError:
        missing_raises = True
    return {
        "dynamic_value": dynamic_val,
        "hasattr_dynamic": hasattr_dynamic,
        "missing_raises": missing_raises,
        "getattr_default": getattr(obj, "dynamic_bar", None),
    }


def demo_proxy_dynamic() -> dict[str, object]:
    """Proxy provides attribute dynamically and forwards to target."""

    target = WithClassGetattr()
    target.existing_class_attr = "target-present"
    proxy = ForwardingProxy(target)
    dynamic_via_proxy = proxy.dynamic_foo  # type: ignore[attr-defined]
    forwarded = proxy.existing_class_attr  # type: ignore[attr-defined]
    try:
        _ = proxy.nonexistent_xyz  # type: ignore[attr-defined]
        missing_raises = False
    except AttributeError:
        missing_raises = True
    return {
        "dynamic_value": dynamic_via_proxy,
        "forwarded": forwarded,
        "hasattr_dynamic": hasattr(proxy, "dynamic_foo"),
        "missing_raises": missing_raises,
        "hasattr_missing_false": not hasattr(proxy, "nonexistent_xyz"),
    }


def demo_monkey_patch_before_use() -> dict[str, object]:
    """Monkey-patching before use makes a dangling attribute present."""

    obj = TrueDangling()
    before = hasattr(obj, "patched_attr")
    # Monkey-patch the class before attribute access.
    TrueDangling.patched_attr = "now-present"  # type: ignore[attr-defined]
    after = hasattr(obj, "patched_attr")
    val = getattr(obj, "patched_attr", None)
    # Cleanup to avoid leakage.
    delattr(TrueDangling, "patched_attr")
    return {"before": before, "after": after, "value": val}


def all_dangling_demos() -> dict[str, object]:
    """Collect dangling vs dynamic demos."""

    return {
        "true_dangling": demo_true_dangling(),
        "module_dynamic": demo_module_dynamic(),
        "class_dynamic": demo_class_dynamic(),
        "proxy_dynamic": demo_proxy_dynamic(),
        "monkey_patch": demo_monkey_patch_before_use(),
    }
