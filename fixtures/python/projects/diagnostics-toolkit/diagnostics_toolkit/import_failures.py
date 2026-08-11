"""Import failure taxonomy (PY-CAN-DIAG-002).

Covers no-spec ModuleNotFoundError, missing-from-name ImportError,
initializer exception, and guarded native-load failure as distinct
runtime import failures.
"""

from __future__ import annotations

import importlib
import importlib.util
import pathlib
import sys


def demo_no_spec_module_not_found() -> dict[str, object]:
    """Trigger ModuleNotFoundError for a top-level missing spec."""

    missing = "diagnostics_toolkit.nonexistent_top_level_xyz"
    try:
        importlib.import_module(missing)
        return {"raised": False}
    except ModuleNotFoundError as exc:
        return {"raised": True, "name": exc.name, "msg": str(exc), "path": getattr(exc, "path", None)}
    except ImportError as exc:  # pragma: no cover - fallback
        return {"raised": True, "name": getattr(exc, "name", None), "fallback": True}


def demo_missing_from_name_import_error() -> dict[str, object]:
    """Trigger ImportError for a missing name inside an existing module."""

    try:
        from diagnostics_toolkit.warnings_toolkit import nonexistent_export_xyz  # type: ignore[attr-defined]

        _ = nonexistent_export_xyz
        return {"raised": False}
    except ImportError as exc:
        return {"raised": True, "name": getattr(exc, "name", None), "path": getattr(exc, "path", None), "msg": str(exc)}


def demo_initializer_exception() -> dict[str, object]:
    """Trigger an exception raised during module initialization."""

    # _failing_initializer raises RuntimeError at import time.
    try:
        importlib.import_module("diagnostics_toolkit._failing_initializer")
        return {"raised": False}
    except RuntimeError as exc:
        return {"raised": True, "kind": "RuntimeError", "msg": str(exc)}
    except ImportError as exc:  # pragma: no cover - import system wraps
        return {"raised": True, "kind": "ImportError", "msg": str(exc)}


def demo_guarded_native_load_failure() -> dict[str, object]:
    """Guard a native-extension load failure without masking transitive errors."""

    native_name = "diagnostics_toolkit._native_missing_c_extension_xyz"
    try:
        importlib.import_module(native_name)
        return {"raised": False}
    except ModuleNotFoundError as exc:
        # Narrow guard inspects name; broad ImportError would mask transitive failures.
        return {"raised": True, "guard": "ModuleNotFoundError", "name": exc.name, "path": getattr(exc, "path", None)}
    except ImportError as exc:
        return {"raised": True, "guard": "ImportError", "name": getattr(exc, "name", None)}


def demo_guarded_import_with_name_inspection() -> dict[str, object]:
    """Show correct inspection of ImportError.name/path versus broad catch."""

    # Attempt a missing module and inspect structured fields rather than message text.
    target = "diagnostics_toolkit.missing_for_inspection_demo_xyz"
    try:
        importlib.import_module(target)
        return {"raised": False}
    except ModuleNotFoundError as exc:
        inspected_name = exc.name
        inspected_path = getattr(exc, "path", None)
        assert inspected_name == target or target in str(inspected_name or "")
        return {"raised": True, "inspected_name": inspected_name, "inspected_path": inspected_path}


def demo_transitive_failure_not_masked() -> dict[str, object]:
    """Transitive initializer failure must not be swallowed by a broad optional catch."""

    # The failing initializer raises RuntimeError, not ImportError, so a narrow
    # ModuleNotFoundError guard would not catch it.
    try:
        importlib.import_module("diagnostics_toolkit._failing_initializer")
        return {"masked": False, "raised": False}
    except ModuleNotFoundError:
        # Incorrect broad handling would land here; we explicitly do not.
        return {"masked": True}
    except RuntimeError as exc:
        return {"masked": False, "raised": True, "msg": str(exc)}


def all_import_failure_demos() -> dict[str, object]:
    """Run every import-failure variant and collect structured results."""

    return {
        "no_spec": demo_no_spec_module_not_found(),
        "missing_name": demo_missing_from_name_import_error(),
        "initializer": demo_initializer_exception(),
        "native_guarded": demo_guarded_native_load_failure(),
        "name_inspection": demo_guarded_import_with_name_inspection(),
        "transitive": demo_transitive_failure_not_masked(),
    }
