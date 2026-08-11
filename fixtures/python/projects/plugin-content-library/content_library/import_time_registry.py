"""Import-time execution and ordering (PY-CAN-MOD-012).

Demonstrates:

- registry population as import side effect (via ``registry``)
- first-import-only execution (``import_time_registry`` body runs once)
- never-imported module (``never_imported.py``)
- two-name double execution (same file under two module names)
- ordering dependency (import order controls registry order)
- failing initializer (``failing_init_plugin.py`` raises at import)

This module itself registers an entry at import time.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys

from content_library.registry import CONTENT_REGISTRY, register_content

# Import-time side effect: register this module's contribution.
register_content("import_time_registry", {"phase": "import"})

IMPORT_ORDER_NOTE = "registry populated top-to-bottom at first import"

NEVER_IMPORTED_NAME = "content_library.never_imported"

FAILING_PLUGIN_PATH = pathlib.Path(__file__).with_name("failing_init_plugin.py")


def demonstrate_two_name_double_execution() -> dict[str, object]:
    """Load the same file under two distinct module names to force re-execution."""
    src_path = pathlib.Path(__file__).with_name("two_name_plugin.py")
    # Ensure the source exists; it registers on each execution.
    first_spec = importlib.util.spec_from_file_location(
        "content_library.two_name_plugin_a", str(src_path)
    )
    second_spec = importlib.util.spec_from_file_location(
        "content_library.two_name_plugin_b", str(src_path)
    )
    assert first_spec and first_spec.loader and second_spec and second_spec.loader
    first_mod = importlib.util.module_from_spec(first_spec)
    sys.modules[first_spec.name] = first_mod
    first_spec.loader.exec_module(first_mod)
    second_mod = importlib.util.module_from_spec(second_spec)
    sys.modules[second_spec.name] = second_mod
    second_spec.loader.exec_module(second_mod)
    before = CONTENT_REGISTRY.copy()
    # Cleanup duplicate entries so later tests see a single registry.
    for name in (first_spec.name, second_spec.name):
        sys.modules.pop(name, None)
    return {
        "first_a": first_mod.REGISTRATION_KEY,
        "first_b": second_mod.REGISTRATION_KEY,
        "registry_keys_after": list(before.keys()),
    }


def demonstrate_failing_initializer() -> str:
    """Import a module whose top-level raises and show partial state."""
    spec = importlib.util.spec_from_file_location(
        "content_library.failing_init_plugin", str(FAILING_PLUGIN_PATH)
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        return "unexpected-success"
    except RuntimeError as exc:
        return f"failing-initializer:{exc}"
    finally:
        sys.modules.pop(spec.name, None)


def ordering_dependency_demo() -> list[str]:
    """Return registry order after a controlled import sequence."""
    from content_library.registry import REGISTRY_ORDER

    return list(REGISTRY_ORDER)
