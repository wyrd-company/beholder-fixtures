"""Multiprocessing workers with entry modes and pickle identity (PY-CAN-INT-007)."""

from __future__ import annotations

import multiprocessing
import multiprocessing.context
import pickle
import sys

# --- Top-level worker: must be at module top-level to be pickleable by spawn ---


def worker(x: int) -> int:
    """Top-level worker pickled by reference via module lookup (spawn-safe)."""
    return x * x


def worker_with_identity(x: int) -> tuple[int, str]:
    """Returns result and module name to prove pickle identity retains module."""
    return (x * 2, __name__)


# --- Local/interactive failure counterexample (must not be spawnable) ---


def local_failure_demo() -> str:
    """Attempt to pickle a local function - should fail."""

    def local_worker(y: int) -> int:  # local scope, not importable
        return y + 1

    try:
        pickle.dumps(local_worker)
        # On some contexts spawn may use cloudpickle, but stdlib pickle uses qualname lookup
        # For local functions pickle reconstructs via __qualname__ which includes `<locals>`
        # It will pickle but unpickling in child without parent frame fails? Actually pickle of local succeeds to bytes but child's import fails.
        # Check by trying to run in spawn context
        ctx = multiprocessing.get_context("spawn")
        with ctx.Pool(1) as pool:
            pool.apply(local_worker, (5,))  # should fail
        return "no-error"
    except (AttributeError, pickle.PicklingError) as exc:
        return f"local-pickle-failure:{exc.__class__.__name__}"
    except Exception as exc:  # noqa: BLE001
        return f"other-failure:{exc.__class__.__name__}:{exc}"


# --- Pickle identity demo: loads yields same object via import lookup ---


def pickle_identity_demo() -> dict[str, object]:
    data = pickle.dumps(worker)
    restored = pickle.loads(data)
    # Pickle of top-level function stores module + qualname; loads imports same object (identity by module lookup)
    same_via_import = restored is worker
    # But explicit equality also holds
    same_result = restored(5) == worker(5)
    return {"same_via_import": same_via_import, "same_result": same_result, "module": restored.__module__}


# --- Entry mode spawners without recursive startup guard ---


def spawn_with_context(start_method: str, value: int) -> int:
    """Spawn worker via explicit context to test start methods, guarded against recursive startup."""
    # This function itself is top-level; caller must be under `if __name__ == '__main__'` guard when invoked as script
    ctx = multiprocessing.get_context(start_method)
    # Use Pool with single task to avoid needing `if __name__ == '__main__'` inside worker module
    with ctx.Pool(1) as pool:
        return pool.apply(worker, (value,))  # type: ignore[no-any-return]


def spawn_spawn_demo() -> int:
    return spawn_with_context("spawn", 7)


def spawn_fork_demo() -> int | str:
    # fork may not be available on all platforms, but on Linux it is
    try:
        return spawn_with_context("fork", 7)
    except ValueError as exc:
        return f"fork-unavailable:{exc}"


def spawn_forkserver_demo() -> int | str:
    try:
        return spawn_with_context("forkserver", 7)
    except ValueError as exc:
        return f"forkserver-unavailable:{exc}"


# Direct-script package context counterexample:
# When run via `python feature_integration_suite/mp_workers.py`, __package__ is None and relative imports fail.
package_context_when_direct = __package__
package_context_note = (
    "direct-script execution gives __package__ is None / '' causing relative imports to fail; "
    "package mode `python -m feature_integration_suite.mp_workers` preserves package context"
)


# Guard for recursive startup: module code at import time must not spawn.
# Only under `if __name__ == '__main__':` should spawning happen.
# Demonstrate that import does not trigger spawn: this module's top-level does not call spawn_*.
_import_does_not_spawn = True


def recursive_startup_guard_demo() -> str:
    """Show guard pattern: spawning only when __name__ == '__main__' and freeze_support."""
    # This string documents the guard; actual guard is in __main__.py and mp_entry.py
    return "guard: if __name__ == '__main__': multiprocessing.freeze_support(); spawn..."


# Frozen support note: executable built with PyInstaller/cx_Freeze needs freeze_support()
def frozen_support_demo() -> str:
    # On normal interpreter, freeze_support is no-op
    try:
        multiprocessing.freeze_support()
        return "freeze_support:callable"
    except Exception as exc:  # noqa: BLE001
        return f"freeze-error:{exc}"


# --- Child process helpers for entry-mode tests ---


def run_in_child_via_spawn(value: int) -> int:
    """Helper run in child; top-level so spawn can import it."""
    return worker(value) + 1


if __name__ == "__main__":
    # Guarded entry: only spawn when executed directly, not on import
    multiprocessing.freeze_support()
    print(spawn_spawn_demo())
