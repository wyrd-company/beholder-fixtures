"""Metadata inspection helpers for PKG-003, PKG-013."""

from __future__ import annotations

import importlib.metadata as meta


def get_core_metadata() -> meta.Distribution:
    return meta.distribution("distributable-suite-core")


def get_version_via_metadata() -> str:
    return meta.version("distributable-suite-core")


def list_entry_points(group: str = "suite.plugins"):
    eps = meta.entry_points(group=group) if hasattr(meta.entry_points(group=group), "__iter__") else meta.entry_points().get(group, [])
    try:
        return list(meta.entry_points(group=group))
    except TypeError:
        return meta.entry_points().get(group, [])


def static_vs_dynamic_fields() -> dict:
    """Document which fields are static vs dynamic per pyproject.

    Static: name, description, readme, requires-python, dependencies, extras, entry-points
    Dynamic: version (derived from suite_core._generated_version via setuptools attr)
    """
    return {
        "static": ["name", "description", "readme", "requires-python", "dependencies", "optional-dependencies", "entry-points", "scripts"],
        "dynamic": ["version"],
        "dynamic_source": "suite_core._generated_version.__version__",
    }


def resolve_optional_import(extra: str = "visualization") -> str:
    """Guarded optional import pattern for PKG-007."""
    try:
        import importlib

        importlib.import_module(f"suite_core.optional_deps_{extra}")
        return f"{extra}-available"
    except ModuleNotFoundError:
        return f"{extra}-missing-guard-activated"
