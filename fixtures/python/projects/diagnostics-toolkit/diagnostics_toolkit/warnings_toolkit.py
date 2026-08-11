"""Warnings toolkit (PY-CAN-DIAG-004).

Emits custom and deprecation warnings through a wrapper and exercises
capture, error, ignore filters, registries, and caller attribution.
Also supports isolated-process warning-filter demos.
"""

from __future__ import annotations

import subprocess
import sys
import warnings


class ToolkitWarning(UserWarning):
    """Custom toolkit warning."""


class ToolkitDeprecationWarning(DeprecationWarning):
    """Toolkit-specific deprecation warning."""


def _emit_via_wrapper(
    message: str,
    category: type[Warning] = ToolkitWarning,
    stacklevel: int = 2,
) -> None:
    """Wrapper that emits via warnings.warn with configurable stacklevel."""

    warnings.warn(message, category, stacklevel=stacklevel)


def emit_custom(message: str = "toolkit custom warning") -> None:
    """Emit ToolkitWarning through the wrapper."""

    _emit_via_wrapper(message, ToolkitWarning, stacklevel=2)


def emit_deprecation(message: str = "deprecated toolkit API") -> None:
    """Emit ToolkitDeprecationWarning through the wrapper."""

    _emit_via_wrapper(message, ToolkitDeprecationWarning, stacklevel=2)


def emit_with_explicit_stacklevel() -> tuple[str, int]:
    """Emit with stacklevel=3 and return caller attribution info."""

    # Wrapper chain: caller -> intermediate -> _emit_via_wrapper
    def intermediate() -> None:
        _emit_via_wrapper("attributed", ToolkitWarning, stacklevel=3)

    intermediate()
    return ("attributed", 3)


def demo_capture_filter() -> list[warnings.WarningMessage]:
    """Capture warnings using the 'always' filter."""

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", ToolkitWarning)
        emit_custom("captured-one")
        emit_custom("captured-two")
        return captured


def demo_error_filter() -> dict[str, object]:
    """Turn a warning category into an error."""

    with warnings.catch_warnings():
        warnings.filterwarnings("error", category=ToolkitWarning)
        try:
            emit_custom("should-error")
            return {"raised": False}
        except ToolkitWarning as exc:
            return {"raised": True, "kind": "ToolkitWarning", "msg": str(exc)}
        except Warning as exc:  # pragma: no cover
            return {"raised": True, "kind": type(exc).__name__}


def demo_ignore_filter() -> list[warnings.WarningMessage]:
    """Ignore a warning category."""

    with warnings.catch_warnings(record=True) as captured:
        warnings.filterwarnings("ignore", category=ToolkitWarning)
        # Also ensure Deprecation not hidden interferes? filter only ToolkitWarning
        warnings.simplefilter("ignore", ToolkitWarning)
        emit_custom("ignored-one")
        emit_deprecation("ignored-deprecation")  # different category still maybe hidden differently
        return captured


def demo_registry_behavior() -> dict[str, object]:
    """Exercise the per-module warning registry."""

    mod = sys.modules[__name__]
    # Clear prior registry entry if present.
    registry = getattr(mod, "__warningregistry__", None)
    if isinstance(registry, dict):
        registry.clear()
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always", ToolkitWarning)
        emit_custom("registry-first")
        first_registry = dict(getattr(mod, "__warningregistry__", {}))
        emit_custom("registry-second")
        second_registry = dict(getattr(mod, "__warningregistry__", {}))
    return {
        "first_keys": sorted(first_registry.keys()),
        "second_keys": sorted(second_registry.keys()),
        "has_registry": hasattr(mod, "__warningregistry__"),
    }


def demo_caller_attribution() -> dict[str, object]:
    """Verify wrapper stacklevel attributes warning to the caller."""

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", ToolkitWarning)

        def caller() -> None:
            emit_custom("attribution-check")

        caller()
        if not captured:
            return {"captured": False}
        w = captured[0]
        # filename should be this file, lineno should point near caller()
        return {
            "captured": True,
            "filename": w.filename,
            "lineno": w.lineno,
            "message": str(w.message),
            "category": w.category.__name__,
        }


def demo_isolated_warning_filters() -> dict[str, object]:
    """Run warning-filter variants in an isolated child process."""

    code = """
import warnings, sys
from diagnostics_toolkit.warnings_toolkit import emit_custom, emit_deprecation, ToolkitWarning, ToolkitDeprecationWarning

# capture
with warnings.catch_warnings(record=True) as cap:
    warnings.simplefilter("always", ToolkitWarning)
    emit_custom("child-capture")
    print("capture", len(cap))

# error
with warnings.catch_warnings():
    warnings.filterwarnings("error", category=ToolkitWarning)
    try:
        emit_custom("child-error")
        print("error not-raised")
    except ToolkitWarning:
        print("error raised")

# ignore
with warnings.catch_warnings(record=True) as cap2:
    warnings.filterwarnings("ignore", category=ToolkitWarning)
    warnings.simplefilter("ignore", ToolkitWarning)
    emit_custom("child-ignore")
    print("ignore", len(cap2))

# registry
import diagnostics_toolkit.warnings_toolkit as wt
if hasattr(wt, "__warningregistry__"):
    wt.__warningregistry__.clear()
with warnings.catch_warnings(record=True):
    warnings.simplefilter("always", ToolkitWarning)
    emit_custom("child-registry")
    reg = getattr(wt, "__warningregistry__", {})
    print("registry", bool(reg))
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "returncode": result.returncode,
        "stdout": result.stdout.strip().splitlines(),
        "stderr": result.stderr.strip(),
    }


def all_warning_demos() -> dict[str, object]:
    """Collect warning variant demos."""

    return {
        "capture": len(demo_capture_filter()),
        "error": demo_error_filter(),
        "ignore": len(demo_ignore_filter()),
        "registry": demo_registry_behavior(),
        "attribution": demo_caller_attribution(),
        "isolated": demo_isolated_warning_filters(),
    }
