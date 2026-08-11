"""Search paths, shadowing, and source roots (PY-CAN-MOD-016).

Contrasts flat and ``src`` layouts and resolves two candidates for one name.
Demonstrates ``PYTHONPATH`` / ``sys.path`` ordering, editable ``.pth``,
and shadowing hazards (standard-library, case-insensitive).

Layouts are separate configurations:

- ``flat_layout/search_demo.py``  (flat)
- ``src_layout/src/search_demo.py`` (src layout, requires ``src_layout/src`` on path)
"""

from __future__ import annotations

import pathlib
import sys


def flat_vs_src_demo() -> dict[str, str]:
    import importlib
    import importlib.util

    project_root = pathlib.Path(__file__).parent.parent
    flat_path = project_root / "flat_layout"
    src_path = project_root / "src_layout" / "src"

    # Flat layout: directory on path directly contains ``search_demo.py``.
    # Use spec_from_file_location to emulate without polluting sys.path ordering.
    flat_spec = importlib.util.spec_from_file_location(
        "search_demo_flat", str(flat_path / "search_demo.py")
    )
    src_spec = importlib.util.spec_from_file_location(
        "search_demo_src", str(src_path / "search_demo.py")
    )
    assert flat_spec and flat_spec.loader and src_spec and src_spec.loader
    flat_mod = importlib.util.module_from_spec(flat_spec)
    flat_spec.loader.exec_module(flat_mod)  # type: ignore
    src_mod = importlib.util.module_from_spec(src_spec)
    src_spec.loader.exec_module(src_mod)  # type: ignore
    return {"flat": flat_mod.VALUE, "src": src_mod.VALUE}  # type: ignore


def path_order_shadowing_demo() -> dict[str, str]:
    """Two candidates for ``shadow_candidate`` — first on sys.path wins."""
    import tempfile
    import pathlib as pl

    with tempfile.TemporaryDirectory() as tmp_a, tempfile.TemporaryDirectory() as tmp_b:
        pa = pl.Path(tmp_a)
        pb = pl.Path(tmp_b)
        (pa / "shadow_candidate.py").write_text('VALUE = "from-a"\n')
        (pb / "shadow_candidate.py").write_text('VALUE = "from-b"\n')
        # Ordering: A before B
        sys.path.insert(0, str(pa))
        sys.path.insert(1, str(pb))
        try:
            import importlib

            # Clean any prior
            sys.modules.pop("shadow_candidate", None)
            importlib.invalidate_caches()
            mod = importlib.import_module("shadow_candidate")
            value_first_wins = mod.VALUE  # type: ignore
            # Reorder and show second wins
            sys.path.remove(str(pa))
            sys.path.append(str(pa))
            sys.modules.pop("shadow_candidate", None)
            importlib.invalidate_caches()
            mod2 = importlib.import_module("shadow_candidate")
            value_second_wins = mod2.VALUE  # type: ignore
            return {"first_wins": value_first_wins, "second_wins": value_second_wins}
        finally:
            for p in [str(pa), str(pb)]:
                if p in sys.path:
                    sys.path.remove(p)
            sys.modules.pop("shadow_candidate", None)


def stdlib_shadowing_note() -> str:
    """Local ``json.py`` would shadow stdlib ``json`` if placed early on path."""
    return "hazard: local json.py on sys.path before stdlib shadows the stdlib"


def case_insensitive_note() -> str:
    return "on case-insensitive filesystems Search_Demo.py and search_demo.py collide"


def editable_pth_note() -> str:
    return "editable .pth in site-packages adds project src to sys.path"


def launcher_vs_working_directory_note() -> str:
    return "launcher mode (-m) sets different sys.path[0] than direct script path"
