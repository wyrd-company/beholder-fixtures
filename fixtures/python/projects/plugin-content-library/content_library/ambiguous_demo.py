"""Demonstration helper for PY-CAN-MOD-007 ambiguity variants."""

from __future__ import annotations

from content_library.ambiguous_pkg import handler as attr_handler
import importlib


def demo_attribute_shadowing() -> dict[str, str]:
    # ``from package import handler`` binds the attribute, not the submodule.
    return {"handler": attr_handler, "expected": "attribute-value"}


def demo_submodule_fallback() -> str:
    # No attribute named ``fallback_child`` — falls back to submodule.
    from content_library.ambiguous_pkg import fallback_child

    return fallback_child.__name__


def demo_missing_name() -> str:
    try:
        from content_library.ambiguous_pkg import nonexistent  # type: ignore  # noqa: F401
        return "unexpected-success"
    except ImportError as exc:
        return f"missing-name:{exc}"


def demo_cyclic_timing() -> str:
    # Importing the submodule loads the package first; attribute already set.
    # The submodule can read the package attribute during its own init.
    mod = importlib.import_module("content_library.ambiguous_pkg.handler")
    # The package attribute is still the string, not the module.
    from content_library import ambiguous_pkg

    return f"attr={ambiguous_pkg.handler!r} vs module={mod.HANDLER_MODULE_VALUE!r}"
