"""Dispatch framework fixture package."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

from dispatch_framework.single_dispatch import (
    ambiguous_abc_pair,
    dispatch_for,
    format_value,
    format_value_registry,
    out_of_module_handle,
)
from dispatch_framework.method_dispatch import ChannelDispatcher
from dispatch_framework.namespace_ops import (
    computed_attribute,
    dynamic_export,
    feature_probe,
    resolve_via_vars,
)
from dispatch_framework.dotted_paths import (
    LoaderError,
    build_composed_path,
    factory_create,
    resolve_dotted_path,
)
from dispatch_framework.registries import (
    HandlerRegistry,
    PluginBase,
    RegisteredHandler,
    handler_registry,
)
from dispatch_framework.injection import Container, build_model, injected_call
from dispatch_framework.proxy import Proxy
from dispatch_framework.lazy import HeavyResource, cached_total
from dispatch_framework.commands import build_parser, dispatch_command
from dispatch_framework.models import Field, Model, Relationship
from dispatch_framework.logging_config import get_child_logger

__all__ = [
    "ChannelDispatcher",
    "Container",
    "Field",
    "HandlerRegistry",
    "HeavyResource",
    "LoaderError",
    "Model",
    "PluginBase",
    "Proxy",
    "RegisteredHandler",
    "Relationship",
    "ambiguous_abc_pair",
    "build_composed_path",
    "build_model",
    "build_parser",
    "cached_total",
    "computed_attribute",
    "dispatch_command",
    "dispatch_for",
    "dynamic_export",
    "factory_create",
    "feature_probe",
    "format_value",
    "format_value_registry",
    "get_child_logger",
    "handler_registry",
    "injected_call",
    "out_of_module_handle",
    "resolve_dotted_path",
    "resolve_via_vars",
]

# PEP 562 lazy module export: package-level __getattr__ / __dir__.
_LAZY_EXPORTS: dict[str, str] = {
    "lazy_submodule": "dispatch_framework.lazy_submodule",
}


def __getattr__(name: str) -> Any:
    if name in _LAZY_EXPORTS:
        module = importlib.import_module(_LAZY_EXPORTS[name])
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))
