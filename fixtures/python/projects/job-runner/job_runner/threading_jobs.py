"""Threading and synchronization (PY-CAN-FLOW-009)."""

from __future__ import annotations

import threading


_shared_counter = 0
_shared_counter_lock = threading.Lock()
_thread_local = threading.local()


def shared_counter_without_lock(increments: int) -> int:
    """Update shared state without lock — compound-operation race may lose updates.

    No timing assertion is made; the function simply performs the racy pattern.
    """
    global _shared_counter
    _shared_counter = 0

    def worker() -> None:
        global _shared_counter
        for _ in range(increments):
            # Compound: read-modify-write not atomic even under GIL
            tmp = _shared_counter
            tmp += 1
            _shared_counter = tmp

    threads = [threading.Thread(target=worker) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return _shared_counter


def shared_counter_with_lock(increments: int) -> int:
    """Update shared state with lock — protected increment."""
    global _shared_counter
    _shared_counter = 0

    def worker() -> None:
        global _shared_counter
        for _ in range(increments):
            with _shared_counter_lock:
                tmp = _shared_counter
                tmp += 1
                _shared_counter = tmp

    threads = [threading.Thread(target=worker) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return _shared_counter


def thread_local_state(thread_count: int = 3) -> dict[str, object]:
    """Thread-local storage isolates per-thread state."""
    results: dict[int, str] = {}

    def worker(n: int) -> None:
        _thread_local.job_label = f"job-{n}"
        # Simulate work without sleep-based timing assertion
        results[n] = _thread_local.job_label

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(thread_count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return {"results": results, "main_has_local": hasattr(_thread_local, "job_label")}


def capture_thread_failure() -> dict[str, object]:
    """Capture exception from thread without timing assertion."""

    errors: list[str] = []

    def failing_worker() -> None:
        raise ValueError("worker-failure")

    # Custom thread that captures exception
    class CapturingThread(threading.Thread):
        def __init__(self) -> None:
            super().__init__(target=failing_worker)
            self.captured: BaseException | None = None

        def run(self) -> None:
            try:
                super().run()
            except BaseException as exc:  # noqa: BLE001
                self.captured = exc

    t = CapturingThread()
    t.start()
    t.join()
    if t.captured is not None:
        errors.append(type(t.captured).__name__)

    # Alternative: exception inside target handled locally
    handled: list[str] = []

    def handled_worker() -> None:
        try:
            raise RuntimeError("handled-inside")
        except RuntimeError as exc:
            handled.append(type(exc).__name__)

    t2 = threading.Thread(target=handled_worker)
    t2.start()
    t2.join()

    return {"captured": errors, "handled": handled}


def daemon_shutdown_note() -> str:
    """Daemon threads do not prevent interpreter exit; non-daemon do."""
    t = threading.Thread(target=lambda: None, daemon=True)
    t.start()
    t.join()
    return "daemon-threads-do-not-block-shutdown"


def compound_operation_race_note() -> str:
    """Compound read-modify-write is not atomic; C extensions may release GIL."""
    return "compound-race-c-extension-may-release-gil-free-threaded-excluded"


def gil_build_note() -> str:
    """Fixture runs on standard GIL-enabled build; free-threaded lane excluded."""
    return "gil-enabled-build-no-free-threaded"
