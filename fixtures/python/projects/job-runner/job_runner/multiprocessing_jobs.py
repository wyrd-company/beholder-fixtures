"""Multiprocessing start methods (PY-CAN-FLOW-010)."""

from __future__ import annotations

import multiprocessing


def top_level_worker(payload: int) -> int:
    """Importable top-level worker for spawn compatibility."""
    return payload * 2


def _run_with_context(method: str, payloads: list[int]) -> list[int]:
    ctx = multiprocessing.get_context(method)
    with ctx.Pool(processes=2) as pool:
        return pool.map(top_level_worker, payloads)


def run_with_spawn(payloads: list[int]) -> list[int]:
    """Run worker under spawn start method."""
    return _run_with_context("spawn", payloads)


def run_with_fork(payloads: list[int]) -> list[int]:
    """Run worker under fork start method (Linux)."""
    return _run_with_context("fork", payloads)


def run_with_forkserver(payloads: list[int]) -> list[int]:
    """Run worker under forkserver start method (Linux)."""
    return _run_with_context("forkserver", payloads)


def main_guard_note() -> str:
    """Main guard prevents recursive spawning under spawn/forkserver."""
    return "if __name__ == '__main__': guard required for spawn"


def pickling_failure_notes() -> dict[str, str]:
    """Local and lambda callables cannot be pickled for multiprocessing."""
    # These forms would fail if sent to a Pool:
    #   pool.map(lambda x: x*2, ...)
    #   def outer(): def local(x): ...; pool.map(local, ...)
    # Captured as documentation of the failure mode, not executed as failure.
    failures: dict[str, str] = {}
    import pickle

    try:
        pickle.dumps(lambda x: x)
        failures["lambda"] = "pickled-unexpectedly"
    except Exception as exc:  # noqa: BLE001
        failures["lambda"] = type(exc).__name__

    def outer() -> None:
        def local_worker(x: int) -> int:
            return x

        try:
            pickle.dumps(local_worker)
            failures["local"] = "pickled-unexpectedly"
        except Exception as exc:  # noqa: BLE001
            failures["local"] = type(exc).__name__

    outer()
    return failures


def platform_default_variance_note() -> str:
    """Default start method varies by platform; Linux default is fork."""
    return f"default-{multiprocessing.get_start_method(allow_none=True)}-available-{multiprocessing.get_all_start_methods()}"


def fork_with_threads_hazard_note() -> str:
    """Forking a multithreaded process may deadlock; spawn/forkserver safer."""
    return "fork-with-threads-hazard-prefer-spawn"


def propagated_error_demo() -> str:
    """Worker exception propagates to parent via Pool."""
    try:
        ctx = multiprocessing.get_context("spawn")
        def _failing_worker(x: int) -> int:
            raise ValueError("worker-error")

        # Use top-level wrapper to propagate
        with ctx.Pool(processes=1) as pool:
            pool.map(_failing_worker, [1])  # type: ignore[arg-type]
    except Exception as exc:  # noqa: BLE001
        return type(exc).__name__
    return "no-error"


def frozen_support_note() -> str:
    """Frozen executables need multiprocessing.freeze_support()."""
    return "freeze_support-required-for-frozen"


if __name__ == "__main__":
    # Guarded entry for direct execution; spawn re-imports this module.
    multiprocessing.freeze_support()
    result = run_with_spawn([1, 2, 3])
    _ = result
