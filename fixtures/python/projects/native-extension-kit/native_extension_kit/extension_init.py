"""PY-CAN-NATIVE-001: single- and multi-phase initialization, per-module state."""

from __future__ import annotations

import importlib.util
import sys
import sysconfig

# Single-phase extension: m_size == -1, no per-module state, PyMODINIT_FUNC PyInit__native_single
try:
    from . import _native_single  # type: ignore[import-not-found]
except ImportError:
    _native_single = None  # type: ignore[assignment]

# Multi-phase extension: m_size == sizeof(state), Py_mod_exec slot, per-module state
try:
    from . import _native_multi  # type: ignore[import-not-found]
except ImportError:
    _native_multi = None  # type: ignore[assignment]

EXTENSION_SUFFIX = sysconfig.get_config_var("EXT_SUFFIX")
SHLIB_SUFFIX = sysconfig.get_config_var("SHLIB_SUFFIX")


def single_phase_demo() -> dict[str, object]:
    if _native_single is None:
        return {"available": False, "reason": "extension not built"}
    return {
        "available": True,
        "hello": _native_single.owned_new_string("hello-single"),
        "counter_value": _native_single.Counter(7).get_value(),
        "init_style": "single-phase",
        "module_state": "m_size == -1 (no per-module state, global)",
    }


def multi_phase_demo() -> dict[str, object]:
    if _native_multi is None:
        return {"available": False, "reason": "extension not built"}
    before = _native_multi.get_counter()
    _native_multi.increment()
    _native_multi.set_label("demo-label")
    return {
        "available": True,
        "init_style": "multi-phase (PEP 489)",
        "counter_before": before,
        "counter_after": _native_multi.get_counter(),
        "label": _native_multi.get_label(),
        "per_module_state": True,
        "slots": ["Py_mod_exec"],
    }


def per_module_isolation_demo() -> dict[str, object]:
    """Per-module state is per-interpreter import; two spec loads share state via sys.modules
    but demonstrate state API exists. Subinterpreter variant is excluded (unstable high-level API)."""
    if _native_multi is None:
        return {"available": False}
    # Show that state is module-local: two attribute accesses on same module reflect same state
    _native_multi.set_label("isolation-check")
    return {"label": _native_multi.get_label(), "counter": _native_multi.get_counter()}


def extension_suffix_demo() -> dict[str, object]:
    return {
        "ext_suffix": EXTENSION_SUFFIX,
        "shlib_suffix": SHLIB_SUFFIX,
        "example": f"_native_single{EXTENSION_SUFFIX}",
        "linker": "GCC shared -fPIC on Linux x86_64",
    }


def wrong_init_symbol_demo() -> dict[str, object]:
    """Demonstrate wrong init symbol variant isolated: _native_wrong exports PyInit__native_wrong_typo
    so import expecting PyInit__native_wrong fails."""
    import pathlib
    suffix = EXTENSION_SUFFIX or ".so"
    candidate = pathlib.Path(__file__).parent / f"_native_wrong{suffix}"
    if not candidate.exists():
        return {"available": False, "reason": "wrong-init artifact not built", "suffix": suffix}
    spec = importlib.util.spec_from_file_location("_native_wrong", str(candidate))
    if spec is None or spec.loader is None:
        return {"available": False, "reason": "spec creation failed"}
    try:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        return {"available": True, "imported": True, "unexpected": True}
    except ImportError as exc:
        return {"available": True, "import_failed": True, "error": str(exc), "expected": "ImportError due to missing PyInit__native_wrong"}
    except Exception as exc:
        return {"available": True, "import_failed": True, "error": f"{type(exc).__name__}: {exc}"}


__all__ = [
    "single_phase_demo",
    "multi_phase_demo",
    "per_module_isolation_demo",
    "extension_suffix_demo",
    "wrong_init_symbol_demo",
    "EXTENSION_SUFFIX",
]
