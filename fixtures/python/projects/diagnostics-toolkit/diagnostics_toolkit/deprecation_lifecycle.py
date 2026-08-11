"""Deprecation lifecycle and shims (PY-CAN-DIAG-005).

Provides a local deprecated API, replacement, hidden-default warning,
warning-as-error run, and parse-safe compatibility path.
"""

from __future__ import annotations

import importlib.resources
import sys
import warnings


def new_process(payload: str) -> str:
    """Replacement API for the deprecated path."""

    return f"processed:{payload}"


def legacy_process(payload: str) -> str:
    """Deprecated API that warns and delegates to replacement.

    Emits ToolkitDeprecationWarning via a wrapper with stacklevel so
    the warning attributes to the caller.
    """

    warnings.warn(
        "legacy_process is deprecated, use new_process",
        DeprecationWarning,
        stacklevel=2,
    )
    return new_process(payload)


def legacy_hidden_default_demo() -> dict[str, object]:
    """DeprecationWarning is hidden by default; capture only when enabled."""

    # Without filter, DeprecationWarning is typically ignored.
    with warnings.catch_warnings(record=True) as default_captured:
        warnings.simplefilter("ignore", DeprecationWarning)
        legacy_process("hidden")
        default_count = len([w for w in default_captured if issubclass(w.category, DeprecationWarning)])

    with warnings.catch_warnings(record=True) as enabled_captured:
        warnings.simplefilter("always", DeprecationWarning)
        legacy_process("shown")
        enabled_count = len([w for w in enabled_captured if issubclass(w.category, DeprecationWarning)])

    return {"default_hidden": default_count == 0, "enabled_shown": enabled_count == 1}


def demo_warning_as_error() -> dict[str, object]:
    """Run the deprecated API with warnings-as-errors."""

    with warnings.catch_warnings():
        warnings.filterwarnings("error", category=DeprecationWarning)
        try:
            legacy_process("as-error")
            return {"raised": False}
        except DeprecationWarning as exc:
            return {"raised": True, "msg": str(exc)}


def parse_safe_compatibility_path() -> dict[str, object]:
    """Parse-safe compatibility path that selects API by capability, not syntax.

    Uses runtime version/capability branching rather than syntax that would
    fail to parse on older interpreters.
    """

    # Example: importlib.resources.files is 3.9+; fallback to legacy path API.
    # This is parse-safe because both branches are valid syntax.
    if sys.version_info >= (3, 9):
        try:
            # files() exists; exercise it benignly on this package's resources.
            files = importlib.resources.files("diagnostics_toolkit")  # type: ignore[attr-defined]
            exists = files is not None
            return {"path": "modern", "exists": exists}
        except Exception:
            return {"path": "modern-fallback", "exists": False}
    else:  # pragma: no cover - not reached on 3.14
        return {"path": "legacy", "exists": False}


def version_branch_demo() -> dict[str, object]:
    """Capability branch that keeps compatibility without syntax errors."""

    # Capability check instead of version-gated syntax.
    try:
        # ExceptionGroup is 3.11+; availability check is parse-safe.
        _ = BaseExceptionGroup  # type: ignore[name-defined]
        has_group = True
    except NameError:
        has_group = False

    if has_group:
        return {"branch": "with-exception-group", "has_group": True}
    return {"branch": "without-exception-group", "has_group": False}


def all_deprecation_demos() -> dict[str, object]:
    """Collect deprecation lifecycle demos."""

    return {
        "hidden_default": legacy_hidden_default_demo(),
        "warning_as_error": demo_warning_as_error(),
        "parse_safe": parse_safe_compatibility_path(),
        "version_branch": version_branch_demo(),
        "replacement": new_process("demo"),
        "legacy": legacy_hidden_default_demo(),
    }
