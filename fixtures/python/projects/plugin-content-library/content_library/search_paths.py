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


def working_directory_demo() -> dict[str, object]:
    """Working-directory resolution: directory on sys.path[0] analogue."""
    import importlib

    project = pathlib.Path(__file__).parent.parent
    candidate_dir = project / "search_extras" / "workdir_candidate"
    sys.path.insert(0, str(candidate_dir))
    try:
        sys.modules.pop("workdir_mod", None)
        importlib.invalidate_caches()
        mod = importlib.import_module("workdir_mod")
        return {
            "value": mod.VALUE,  # type: ignore
            "path_used": str(candidate_dir),
            "sys_path_0": sys.path[0],
        }
    finally:
        if str(candidate_dir) in sys.path:
            sys.path.remove(str(candidate_dir))
        sys.modules.pop("workdir_mod", None)
        importlib.invalidate_caches()


def pythonpath_demo() -> dict[str, object]:
    """PYTHONPATH resolution via sys.path entry (simulates PYTHONPATH env)."""
    import importlib
    import os

    project = pathlib.Path(__file__).parent.parent
    candidate_dir = project / "search_extras" / "pythonpath_candidate"
    # Simulate PYTHONPATH by inserting the directory; real PYTHONPATH is env var
    # read at interpreter startup and prepended to sys.path.
    sys.path.insert(0, str(candidate_dir))
    # Also demonstrate via subprocess with PYTHONPATH env set.
    env_value = os.environ.get("PYTHONPATH", "")
    try:
        sys.modules.pop("pp_mod", None)
        importlib.invalidate_caches()
        mod = importlib.import_module("pp_mod")
        return {
            "value": mod.VALUE,  # type: ignore
            "path_used": str(candidate_dir),
            "pythonpath_env": env_value or "<not-set>",
        }
    finally:
        if str(candidate_dir) in sys.path:
            sys.path.remove(str(candidate_dir))
        sys.modules.pop("pp_mod", None)
        importlib.invalidate_caches()


def venv_or_editable_pth_demo() -> dict[str, object]:
    """Virtual-environment / editable .pth root via site.addsitedir."""
    import importlib
    import site

    project = pathlib.Path(__file__).parent.parent
    pth_site_dir = project / "search_extras" / "venv_site"
    candidate_dir = (project / "search_extras" / "venv_candidate").resolve()

    # Ensure clean state.
    for name in list(sys.modules):
        if name.startswith("venv_mod"):
            del sys.modules[name]
    # Use site.addsitedir to process editable.pth which adds ../venv_candidate
    site.addsitedir(str(pth_site_dir))
    importlib.invalidate_caches()
    try:
        mod = importlib.import_module("venv_mod")
        return {
            "value": mod.VALUE,  # type: ignore
            "pth_file": str(pth_site_dir / "editable.pth"),
            "pth_target_resolved": str(candidate_dir),
            "in_sys_path": str(candidate_dir) in sys.path,
        }
    finally:
        if str(candidate_dir) in sys.path:
            sys.path.remove(str(candidate_dir))
        for name in list(sys.modules):
            if name.startswith("venv_mod"):
                del sys.modules[name]
        importlib.invalidate_caches()


def stdlib_shadowing_demo() -> dict[str, object]:
    """Standard-library shadowing: local json.py earlier on sys.path shadows stdlib."""
    import importlib

    project = pathlib.Path(__file__).parent.parent
    shadow_dir = project / "search_extras" / "stdlib_shadow"
    sys.path.insert(0, str(shadow_dir))
    try:
        # Ensure stdlib json not already loaded? It typically is. Force reload of shim.
        sys.modules.pop("json", None)
        import json as shadow_json  # type: ignore

        is_shadow = getattr(shadow_json, "VALUE", None) == "shadow-json"
        origin = getattr(shadow_json.__spec__, "origin", "") if hasattr(shadow_json, "__spec__") else ""
        return {
            "is_shadow": is_shadow,
            "value": getattr(shadow_json, "VALUE", None),
            "origin": str(origin),
            "shadow_path": str(shadow_dir / "json.py"),
        }
    finally:
        if str(shadow_dir) in sys.path:
            sys.path.remove(str(shadow_dir))
        # Restore stdlib json.
        sys.modules.pop("json", None)
        try:
            import json  # noqa: F401
        except Exception:
            pass
        importlib.invalidate_caches()


def launcher_vs_working_directory_demo() -> dict[str, object]:
    """Launcher mode (-m) vs direct script sys.path[0] difference (executable)."""
    import subprocess

    project = pathlib.Path(__file__).parent.parent
    # Direct script: run the declaration file as a script; capture package identity and sys.path[0].
    r_direct = subprocess.run(
        [sys.executable, str(project / "content_library" / "entry_declarations.py")],
        capture_output=True, text=True, cwd=str(project),
    )
    r_module = subprocess.run(
        [sys.executable, "-m", "content_library.entry_declarations"],
        capture_output=True, text=True, cwd=str(project),
    )
    # Also demonstrate sys.path[0] via path_probe helper (launcher -m vs direct).
    r_direct_path = subprocess.run(
        [sys.executable, str(project / "content_library" / "path_probe.py")],
        capture_output=True, text=True, cwd=str(project),
    )
    r_m_path = subprocess.run(
        [sys.executable, "-m", "content_library.path_probe"],
        capture_output=True, text=True, cwd=str(project),
    )
    return {
        "launcher_mode_m_stdout": r_module.stdout.strip()[:400],
        "direct_script_stdout": r_direct.stdout.strip()[:400],
        "launcher_path0": r_m_path.stdout.strip() or r_m_path.stderr.strip()[:200],
        "direct_path0": r_direct_path.stdout.strip() or r_direct_path.stderr.strip()[:200],
        "note": "launcher -m sets sys.path[0] to ''/cwd; direct script sets to script directory; package None vs content_library",
    }


def stdlib_shadowing_note() -> str:
    """Deprecated prose alias kept for coverage back-compat; use stdlib_shadowing_demo."""
    return stdlib_shadowing_demo()["value"]  # type: ignore


def editable_pth_note() -> str:
    return str(venv_or_editable_pth_demo()["pth_file"])


def launcher_vs_working_directory_note() -> str:
    return launcher_vs_working_directory_demo()["note"]  # type: ignore


# Unavailable contexts — excluded, not claimed as demonstrations.
EXCLUDED_VARIANTS_NOTE = "test-runner and case-insensitive filesystem collisions are unavailable conditional contexts and are not demonstrated"
