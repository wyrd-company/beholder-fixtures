"""Conditional and local imports (PY-CAN-MOD-011).

Variants:

- platform / version / optional-dependency guards
- narrow vs broad ``ImportError`` handling
- fallback API mismatch documentation
- function-local cycle breaker (repeated calls reuse cache)
- unreachable branch must still parse
"""

from __future__ import annotations

import sys

# Platform guard — Linux-specific branch.
if sys.platform.startswith("linux"):
    import os as platform_module
else:
    import sys as platform_module  # type: ignore

# Version guard.
if sys.version_info >= (3, 11):
    import tomllib as version_module  # type: ignore
else:
    import json as version_module  # type: ignore

# Optional-dependency guard with narrow ``ModuleNotFoundError``.
try:
    import nonexistent_optional  # type: ignore  # noqa: F401
    optional_available = True
except ModuleNotFoundError:
    optional_available = False
    nonexistent_optional = None  # type: ignore

# Broad vs narrow ImportError: broad catches any ImportError (including
# exception inside the imported module), narrow only ModuleNotFoundError.
def broad_import_guard() -> str:
    try:
        import content_library.import_error_plugin  # noqa: F401
        return "unexpected-success"
    except ImportError:
        return "broad-caught-import-error"
    except Exception:
        return "other"


def narrow_import_guard() -> str:
    try:
        import nonexistent_conditional_target  # type: ignore  # noqa: F401
        return "unexpected-success"
    except ModuleNotFoundError:
        return "narrow-caught-not-found"


# Fallback API mismatch: fallback provides different signature but still importable.
try:
    from content_library.nonexistent_fallback import get_value  # type: ignore  # noqa: F401
except ImportError:
    def get_value() -> str:  # type: ignore[no-redef]
        return "fallback-value"


# Function-local cycle breaker — import inside function avoids top-level cycle.
def local_cycle_breaker() -> str:
    import content_library.cycles.a as local_a  # noqa: F401
    return local_a.value_a


# Repeated calls reuse cache: import is executed once, second call returns same object.
def repeated_cache_demo() -> bool:
    import importlib

    first = importlib.import_module("content_library.registry")
    second = importlib.import_module("content_library.registry")
    return first is second


# Unreachable branch must still parse (never executed, but must be valid syntax).
if False:  # pragma: no cover
    import content_library.never_imported as unreachable_import  # type: ignore  # noqa: F401

    unreachable_binding = unreachable_import.VALUE
else:
    unreachable_binding = "reachable"

# Keep branch-parsing helper reachable for graph analysis.
UNREACHABLE_DEMO = unreachable_binding
