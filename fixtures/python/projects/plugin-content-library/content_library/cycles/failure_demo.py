"""Failing early ``from`` access within a cycle (PY-CAN-MOD-010).

Two temporary modules are created on the fly that form a cycle where
one uses ``from X import name`` before ``name`` exists, raising
``ImportError``. The sibling ``cycles.a/b`` pair shows the safe
``import module`` + late attribute access that avoids the failure.
"""

from __future__ import annotations

import pathlib
import sys
import tempfile
import importlib.util


def failing_from_import_cycle() -> str:
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp) / "cycle_fail"
        root.mkdir()
        (root / "__init__.py").write_text("")
        (root / "x.py").write_text(
            "from cycle_fail.y import value_y\nvalue_x = 'x'\n"
        )
        (root / "y.py").write_text(
            "from cycle_fail.x import value_x\nvalue_y = 'y'\n"
        )
        sys.path.insert(0, tmp)
        try:
            import importlib

            try:
                importlib.import_module("cycle_fail.x")
                return "unexpected-success"
            except ImportError as exc:
                return f"cycle-from-failed:{exc.__class__.__name__}"
            finally:
                for name in list(sys.modules):
                    if name.startswith("cycle_fail"):
                        del sys.modules[name]
                importlib.invalidate_caches()
        finally:
            sys.path.remove(tmp)


def sys_modules_demo() -> dict[str, object]:
    import sys
    import importlib

    mod = importlib.import_module("content_library.cycles.a")
    present = "content_library.cycles.a" in sys.modules
    # Simulate failed import cleanup: a module that raises is removed from sys.modules.
    failing_name = "content_library.failing_pkg"
    try:
        importlib.import_module(failing_name)
    except RuntimeError:
        pass
    cleaned = failing_name not in sys.modules
    return {"present": present, "failed_cleaned": cleaned, "duplicate_is_same": mod is sys.modules["content_library.cycles.a"]}
