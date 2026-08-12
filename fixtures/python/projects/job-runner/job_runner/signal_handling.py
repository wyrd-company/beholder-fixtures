"""Signals and asynchronous interruption (PY-CAN-FLOW-012). POSIX only."""

from __future__ import annotations

import signal
import threading
import time


def install_and_restore_handler() -> dict[str, str]:
    """Install benign handler and restore previous."""
    received: list[int] = []

    def handler(signum: int, frame) -> None:  # noqa: ANN001
        received.append(signum)

    old = signal.getsignal(signal.SIGUSR1)
    signal.signal(signal.SIGUSR1, handler)
    try:
        # Deliver to self; main-thread delivery is synchronous at interruption boundary
        signal.raise_signal(signal.SIGUSR1)
        return {"installed": "yes", "received": str(len(received))}
    finally:
        signal.signal(signal.SIGUSR1, old)


def main_thread_delivery_note() -> str:
    """Signals are delivered only to main thread."""
    return "signals-delivered-to-main-thread-only"


def interruption_boundary() -> dict[str, str]:
    """Handler runs at interruption boundary of blocking call."""

    interrupted = False

    def handler(signum: int, frame) -> None:  # noqa: ANN001
        nonlocal interrupted
        interrupted = True

    old = signal.getsignal(signal.SIGUSR1)
    signal.signal(signal.SIGUSR1, handler)
    try:
        # Blocking sleep can be interrupted; handler runs before sleep returns
        def _raise_soon() -> None:
            time.sleep(0.02)
            signal.raise_signal(signal.SIGUSR1)

        t = threading.Thread(target=_raise_soon)
        t.start()
        try:
            time.sleep(0.1)
        except InterruptedError:
            interrupted = True
        t.join()
        return {"interrupted": str(interrupted)}
    finally:
        signal.signal(signal.SIGUSR1, old)


def handler_registration_restriction() -> str:
    """Handler registration is only allowed in main thread."""

    error_name = "none"
    result: list[str] = []

    def try_register_in_thread() -> None:
        nonlocal error_name
        try:
            signal.signal(signal.SIGUSR2, lambda s, f: None)
        except ValueError as exc:
            error_name = type(exc).__name__
            result.append(error_name)

    t = threading.Thread(target=try_register_in_thread)
    t.start()
    t.join()
    return error_name or result[0] if result else "no-error"


def posix_signal_set() -> list[str]:
    """POSIX signal set available on Linux; Windows set excluded."""
    # Enumerate a few POSIX signals guaranteed on Linux
    names: list[str] = []
    for name in ("SIGUSR1", "SIGUSR2", "SIGTERM", "SIGALRM", "SIGHUP", "SIGCHLD"):
        if hasattr(signal, name):
            names.append(name)
    return names


def wakeup_descriptor_demo() -> dict[str, str]:
    """Bounded set_wakeup_fd use that restores prior descriptor (POSIX)."""
    import os

    r_fd, w_fd = os.pipe()
    try:
        os.set_blocking(w_fd, False)
    except OSError:
        pass
    old_fd = -1
    old_handler = signal.getsignal(signal.SIGUSR1)
    restored = "unknown"
    try:
        signal.signal(signal.SIGUSR1, lambda s, f: None)
        old_fd = signal.set_wakeup_fd(w_fd, warn_on_full_buffer=False)
        signal.raise_signal(signal.SIGUSR1)
        restored = "true"
    finally:
        try:
            signal.signal(signal.SIGUSR1, old_handler)
        except Exception:
            pass

        try:
            signal.set_wakeup_fd(old_fd, warn_on_full_buffer=False)
        except Exception:
            try:
                signal.set_wakeup_fd(-1, warn_on_full_buffer=False)
            except Exception:
                pass
        try:
            os.close(r_fd)
        except OSError:
            pass
        try:
            os.close(w_fd)
        except OSError:
            pass
    return {"wakeup_fd_set": restored, "old_fd": str(old_fd)}


def wakeup_descriptor_note() -> str:
    """Wakeup fd integrates signals with event loop (signal.set_wakeup_fd)."""
    return "wakeup-fd-via-signal.set_wakeup_fd"


def blocking_native_delay_note() -> str:
    """Blocking native call may delay handler until call returns."""
    return "blocking-native-may-delay-handler-until-return"


def restore_after_use_demo() -> str:
    """Demonstrate install/restore pattern preserves prior handler."""
    orig = signal.getsignal(signal.SIGALRM)

    def temp_handler(signum, frame):  # noqa: ANN001
        pass

    signal.signal(signal.SIGALRM, temp_handler)
    after_install = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, orig)
    after_restore = signal.getsignal(signal.SIGALRM)
    return f"installed-{after_install is temp_handler}-restored-{after_restore is orig}"
