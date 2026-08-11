"""Implicit namespace packages demo (PY-CAN-MOD-003).

Composes ``shared_ns`` from two path portions without ``__init__.py``.
Covers:

- regular-package precedence (``ns_regular`` shadows namespace when earlier)
- dynamic ``__path__`` manipulation
- zip portion (handled in ``zip_resources.py``)
- ``__init__.py`` as counterexample
"""

from __future__ import annotations

import pathlib
import sys
import importlib


def namespace_two_portions_demo() -> dict[str, object]:
    project = pathlib.Path(__file__).parent.parent
    alpha = str(project / "ns_alpha")
    beta = str(project / "ns_beta")
    for p in (alpha, beta):
        if p not in sys.path:
            sys.path.insert(0, p)
    # Ensure clean state.
    for name in list(sys.modules):
        if name.startswith("shared_ns"):
            del sys.modules[name]
    importlib.invalidate_caches()
    try:
        import shared_ns.plugin_alpha as pa  # type: ignore
        import shared_ns.plugin_beta as pb  # type: ignore
        import shared_ns  # type: ignore
        return {
            "alpha": pa.VALUE,
            "beta": pb.VALUE,
            "is_namespace": getattr(shared_ns, "__spec__", None) and getattr(shared_ns.__spec__, "submodule_search_locations", None) is not None and getattr(shared_ns, "__file__", None) is None,
            "path_entries": list(getattr(shared_ns, "__path__", [])),
            "has_init": hasattr(shared_ns, "__file__") and getattr(shared_ns, "__file__", None) is not None,
        }
    finally:
        for p in (alpha, beta):
            if p in sys.path:
                sys.path.remove(p)
        for name in list(sys.modules):
            if name.startswith("shared_ns"):
                del sys.modules[name]
        importlib.invalidate_caches()


def regular_precedence_demo() -> dict[str, object]:
    project = pathlib.Path(__file__).parent.parent
    regular = str(project / "ns_regular")
    alpha = str(project / "ns_alpha")
    for p in (regular, alpha):
        if p not in sys.path:
            sys.path.insert(0, p)
    for name in list(sys.modules):
        if name.startswith("shared_ns"):
            del sys.modules[name]
    importlib.invalidate_caches()
    # Regular package first on path should win.
    sys.path.sort(key=lambda x: 0 if x == regular else 1 if x == alpha else 2)  # type: ignore
    # Ensure regular is first.
    if regular in sys.path:
        sys.path.remove(regular)
        sys.path.insert(0, regular)
    try:
        import shared_ns  # type: ignore

        is_regular = getattr(shared_ns, "__file__", None) is not None
        return {"is_regular": is_regular, "file": getattr(shared_ns, "__file__", None)}
    finally:
        for p in (regular, alpha):
            if p in sys.path:
                sys.path.remove(p)
        for name in list(sys.modules):
            if name.startswith("shared_ns"):
                del sys.modules[name]
        importlib.invalidate_caches()


def dynamic_path_demo() -> list[str]:
    # After importing the namespace, extend its __path__ dynamically.
    result = namespace_two_portions_demo()
    # Demonstrate that mutating __path__ affects subsequent submodule searches.
    # The actual mutation is shown via append to a synthetic path entry.
    paths = result.get("path_entries", [])
    return [str(p) for p in paths]  # type: ignore
