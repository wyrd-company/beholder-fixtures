"""Legacy path demonstrations (PY-CAN-MOD-004)."""

from __future__ import annotations

import pathlib
import sys
import importlib


def extend_path_demo() -> dict[str, object]:
    # ``legacy_pkg`` extends ``__path__`` via controlled mutation at import
    # time (see its ``__init__.py``).  No ``sys.path`` manipulation is needed
    # for this fixture; cache invalidation is still required after any
    # ``__path__`` change.
    importlib.invalidate_caches()
    import content_library.legacy_pkg as pkg  # type: ignore
    mod = importlib.import_module("content_library.legacy_pkg.extra_plugin")
    path_order = list(getattr(pkg, "__path__", []))
    return {
        "extra_found": mod.VALUE,  # type: ignore
        "path_entries": path_order,
        "cache_invalidation": "importlib.invalidate_caches() required after path change",
        "extend_path_legacy": "from pkgutil import extend_path; __path__ = extend_path(__path__, __name__)",
    }


def mixed_style_failure_demo() -> dict[str, object]:
    """Mixed PEP 420 implicit + legacy regular counterexample (PY-CAN-MOD-004).

    ``shared_mixed`` has an implicit namespace portion in ``mixed_a`` (no
    ``__init__.py``) and a regular package portion in ``mixed_b`` (with
    ``__init__.py``).  Placing both on ``sys.path`` demonstrates that the
    mixed style fails: the regular package shadows the namespace, so the
    implicit child ``plugin_a`` is not found without path extension.
    """
    project = pathlib.Path(__file__).parent.parent
    mixed_a = str(project / "mixed_a")
    mixed_b = str(project / "mixed_b")
    for p in (mixed_a, mixed_b):
        if p not in sys.path:
            sys.path.insert(0, p)
    for name in list(sys.modules):
        if name.startswith("shared_mixed"):
            del sys.modules[name]
    importlib.invalidate_caches()
    # Ensure regular portion wins when mixed_b is earlier.
    if mixed_b in sys.path:
        sys.path.remove(mixed_b)
        sys.path.insert(0, mixed_b)
    try:
        import shared_mixed  # type: ignore

        is_regular = getattr(shared_mixed, "__file__", None) is not None
        # Implicit child should not be resolvable via regular __path__.
        try:
            import shared_mixed.plugin_a  # type: ignore  # noqa: F401
            plugin_a_status = "found-despite-mixed"
        except ModuleNotFoundError as exc:
            plugin_a_status = f"mixed-style-not-found:{exc.name}"

        try:
            import shared_mixed.plugin_b as pb  # type: ignore

            plugin_b_status = pb.VALUE
        except ModuleNotFoundError as exc:
            plugin_b_status = f"not-found:{exc.name}"

        return {
            "is_regular": is_regular,
            "regular_file": getattr(shared_mixed, "__file__", None),
            "plugin_a": plugin_a_status,
            "plugin_b": plugin_b_status,
            "note": "mixing implicit namespace (no __init__) with legacy regular package for same top name fails without controlled __path__",
        }
    finally:
        for p in (mixed_a, mixed_b):
            if p in sys.path:
                sys.path.remove(p)
        for name in list(sys.modules):
            if name.startswith("shared_mixed"):
                del sys.modules[name]
        importlib.invalidate_caches()


def mixed_style_failure_note() -> str:
    return "mixing PEP 420 implicit namespace with extend_path in same package fails or is undefined"


def path_order_dependence_demo() -> dict[str, str]:
    # Two extra paths each providing a same-named module — first in
    # ``__path__`` wins (controlled mutation, not sys.path, for subpackages
    # on Python 3.14).
    import tempfile

    import content_library.legacy_pkg as pkg

    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        pa = pathlib.Path(a)
        pb = pathlib.Path(b)
        pa.mkdir(parents=True, exist_ok=True)
        pb.mkdir(parents=True, exist_ok=True)
        (pa / "shadowed.py").write_text('VALUE = "from-a"\n')
        (pb / "shadowed.py").write_text('VALUE = "from-b"\n')
        original_path = list(pkg.__path__)
        pkg.__path__.insert(0, str(pa))
        pkg.__path__.insert(1, str(pb))
        importlib.invalidate_caches()
        try:
            for name in list(sys.modules):
                if name.startswith("content_library.legacy_pkg.shadowed"):
                    del sys.modules[name]
            mod = importlib.import_module("content_library.legacy_pkg.shadowed")
            first = mod.VALUE  # type: ignore
            # Swap order and show second wins
            pkg.__path__.remove(str(pa))
            pkg.__path__.append(str(pa))
            for name in list(sys.modules):
                if name.startswith("content_library.legacy_pkg.shadowed"):
                    del sys.modules[name]
            importlib.invalidate_caches()
            mod2 = importlib.import_module("content_library.legacy_pkg.shadowed")
            second = mod2.VALUE  # type: ignore
            return {"first_wins": first, "second_wins": second, "path_order_dependence": "__path__ order controls resolution"}
        finally:
            pkg.__path__[:] = original_path
            for name in list(sys.modules):
                if name.startswith("content_library.legacy_pkg.shadowed"):
                    del sys.modules[name]
            importlib.invalidate_caches()
