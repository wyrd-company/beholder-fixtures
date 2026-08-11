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
