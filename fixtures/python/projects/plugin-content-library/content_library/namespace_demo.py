"""Implicit namespace packages demo (PY-CAN-MOD-003).

Composes ``shared_ns`` from two path portions without ``__init__.py``.
Covers:

- regular-package precedence (``ns_regular`` shadows namespace when earlier)
- dynamic ``__path__`` manipulation
- zip/installed portion (``dist/shared_ns_portion.zip``)
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


def dynamic_path_demo() -> dict[str, object]:
    """Dynamically add a new namespace portion after the package exists (PY-CAN-MOD-003)."""
    project = pathlib.Path(__file__).parent.parent
    alpha = str(project / "ns_alpha")
    beta = str(project / "ns_beta")
    dynamic = str(project / "ns_dynamic")
    for p in (alpha, beta):
        if p not in sys.path:
            sys.path.insert(0, p)
    for name in list(sys.modules):
        if name.startswith("shared_ns"):
            del sys.modules[name]
    importlib.invalidate_caches()
    try:
        import shared_ns  # type: ignore
        import shared_ns.plugin_alpha  # type: ignore  # noqa: F401

        initial_entries = list(shared_ns.__path__)  # type: ignore
        # Verify dynamic portion not yet importable.
        try:
            import shared_ns.plugin_dynamic  # type: ignore  # noqa: F401
            before_dynamic = "unexpected-success"
        except ModuleNotFoundError:
            before_dynamic = "not-found-before"

        # Dynamically extend __path__ with new portion.  For PEP 420
        # namespace packages, _NamespacePath does not reliably re-resolve
        # after append, so convert to a plain list and update the spec.
        new_entry = str(pathlib.Path(dynamic) / "shared_ns")
        new_path = list(shared_ns.__path__) + [new_entry]  # type: ignore
        shared_ns.__path__ = new_path  # type: ignore
        # Keep spec in sync (they share object initially, but after reassign they diverge).
        if getattr(shared_ns, "__spec__", None) is not None:
            shared_ns.__spec__.submodule_search_locations = new_path  # type: ignore
        importlib.invalidate_caches()
        import shared_ns.plugin_dynamic as pd  # type: ignore

        after_entries = list(shared_ns.__path__)  # type: ignore
        return {
            "initial_entries": [str(p) for p in initial_entries],
            "before_dynamic": before_dynamic,
            "dynamic_value": pd.VALUE,
            "after_entries": [str(p) for p in after_entries],
            "dynamic_path_added": new_entry,
        }
    finally:
        for p in (alpha, beta):
            if p in sys.path:
                sys.path.remove(p)
        for name in list(sys.modules):
            if name.startswith("shared_ns"):
                del sys.modules[name]
        importlib.invalidate_caches()


def zip_portion_demo() -> dict[str, object]:
    """Zip/installed implicit namespace portion (PY-CAN-MOD-003)."""
    project = pathlib.Path(__file__).parent.parent
    alpha = str(project / "ns_alpha")
    zip_path = str(project / "dist" / "shared_ns_portion.zip")
    for p in (alpha,):
        if p not in sys.path:
            sys.path.insert(0, p)
    sys.path.insert(0, zip_path)
    for name in list(sys.modules):
        if name.startswith("shared_ns"):
            del sys.modules[name]
    importlib.invalidate_caches()
    try:
        import shared_ns.plugin_alpha as pa  # type: ignore
        import shared_ns.plugin_zip as pz  # type: ignore
        import shared_ns  # type: ignore
        return {
            "alpha": pa.VALUE,
            "zip_portion": pz.VALUE,
            "is_namespace": getattr(shared_ns.__spec__, "submodule_search_locations", None) is not None,
            "zip_in_path": zip_path in getattr(shared_ns, "__path__", []),
        }
    finally:
        for p in (alpha, zip_path):
            if p in sys.path:
                sys.path.remove(p)
        for name in list(sys.modules):
            if name.startswith("shared_ns"):
                del sys.modules[name]
        importlib.invalidate_caches()
