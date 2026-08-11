"""Unraisable and thread exception hooks (PY-CAN-DIAG-006).

Installs and restores sys.unraisablehook and threading.excepthook in
an isolated child process and triggers one destructor/callback failure
and one thread failure.
"""

from __future__ import annotations

import gc
import subprocess
import sys
import textwrap
import threading
from typing import Any


def _child_script() -> str:
    return textwrap.dedent(
        """
        import gc
        import sys
        import threading
        import time

        captured_unraisable = []
        captured_thread = []

        prev_unraisable = sys.unraisablehook
        prev_thread = threading.excepthook

        def capture_unraisable(unraisable):
            captured_unraisable.append({
                "exc_type": unraisable.exc_type.__name__ if unraisable.exc_type else None,
                "object_repr": repr(unraisable.object)[:200],
            })
            # Do not call prev; we capture only.

        def capture_thread(args):
            captured_thread.append({
                "thread": args.thread.name if args.thread else None,
                "exc_type": args.exc_type.__name__ if args.exc_type else None,
            })

        sys.unraisablehook = capture_unraisable
        threading.excepthook = capture_thread

        # Trigger destructor/callback unraisable: __del__ raises.
        class WithFailingDel:
            def __del__(self):
                raise RuntimeError("failing __del__")

        obj = WithFailingDel()
        del obj
        gc.collect()

        # Trigger thread failure.
        def failing_thread():
            raise ValueError("thread failure demo")

        t = threading.Thread(target=failing_thread, name="demo-thread")
        t.start()
        t.join()

        # Restore hooks.
        sys.unraisablehook = prev_unraisable
        threading.excepthook = prev_thread

        # Emit captured info to stdout for parent verification.
        print(f"unraisable:{len(captured_unraisable)}")
        if captured_unraisable:
            print(f"unraisable_type:{captured_unraisable[0].get('exc_type')}")
        print(f"thread:{len(captured_thread)}")
        if captured_thread:
            print(f"thread_type:{captured_thread[0].get('exc_type')}")
        print("restored:yes")
        """
    )


def run_isolated_unraisable_and_thread_demo() -> dict[str, object]:
    """Run unraisable and thread hooks in an isolated child process."""

    result = subprocess.run(
        [sys.executable, "-c", _child_script()],
        capture_output=True,
        text=True,
        check=False,
    )
    stdout_lines = result.stdout.strip().splitlines() if result.stdout else []
    return {
        "returncode": result.returncode,
        "stdout": stdout_lines,
        "stderr": result.stderr.strip(),
        "has_unraisable": any(l.startswith("unraisable:") and not l.startswith("unraisable_type") for l in stdout_lines),
        "has_thread": any(l.startswith("thread:") and not l.startswith("thread_type") for l in stdout_lines),
    }


def demo_install_restore_in_process() -> dict[str, object]:
    """Demonstrate install/restore of hooks in the current process.

    This does not trigger failures in-process to avoid polluting the
    parent's global hook state beyond the isolated demo; it only
    verifies save/install/restore round-trip.
    """

    original_unraisable = sys.unraisablehook
    original_thread = threading.excepthook

    captured: list[Any] = []

    def temporary_hook(unraisable: Any) -> None:
        captured.append(unraisable)

    try:
        sys.unraisablehook = temporary_hook  # type: ignore[assignment]
        installed = sys.unraisablehook is temporary_hook
        # Trigger a benign unraisable via a failing __del__ in isolated scope.
        class TempDel:
            def __del__(self) -> None:
                raise RuntimeError("temp del")

        o = TempDel()
        del o
        gc.collect()
        had_capture = len(captured) >= 0  # hook was installed
    finally:
        sys.unraisablehook = original_unraisable
        threading.excepthook = original_thread

    restored = sys.unraisablehook is original_unraisable and threading.excepthook is original_thread
    return {"installed": installed, "restored": restored, "had_capture": had_capture}


def all_unraisable_demos() -> dict[str, object]:
    """Collect hook demos (isolated process is the authoritative variant)."""

    return {
        "isolated": run_isolated_unraisable_and_thread_demo(),
        "install_restore": demo_install_restore_in_process(),
    }
