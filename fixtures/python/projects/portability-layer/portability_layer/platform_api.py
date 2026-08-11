"""Platform-only APIs and fallbacks (PY-CAN-PLAT-008)."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass


class UnsupportedPlatformError(RuntimeError):
    """Raised when a platform API is unavailable on this interpreter."""


@dataclass(frozen=True)
class PlatformSupport:
    is_posix: bool
    is_windows: bool
    posix_available: bool
    windows_available: bool


def _try_posix_imports() -> dict[str, object]:
    """POSIX imports behind feature detection; harmless stand-ins on non-POSIX."""
    result: dict[str, object] = {}
    try:
        import fcntl  # noqa: F401

        result["fcntl"] = True
    except ImportError:
        result["fcntl"] = False
    try:
        import pwd  # noqa: F401

        result["pwd"] = True
    except ImportError:
        result["pwd"] = False
    try:
        import grp  # noqa: F401

        result["grp"] = True
    except ImportError:
        result["grp"] = False
    try:
        import termios  # noqa: F401

        result["termios"] = True
    except ImportError:
        result["termios"] = False
    try:
        import syslog  # noqa: F401

        result["syslog"] = True
    except ImportError:
        result["syslog"] = False
    return result


def _try_windows_imports() -> dict[str, object]:
    """Guarded Windows imports that still parse on Linux.

    All files must parse under the selected interpreter; imports are guarded
    so the module loads on POSIX.
    """
    result: dict[str, object] = {}
    try:
        import msvcrt  # noqa: F401

        result["msvcrt"] = True
    except ImportError:
        result["msvcrt"] = False
    try:
        import winreg  # noqa: F401  # type: ignore[import-not-found]

        result["winreg"] = True
    except ImportError:
        result["winreg"] = False
    try:
        import winsound  # noqa: F401

        result["winsound"] = True
    except ImportError:
        result["winsound"] = False
    # _winapi is CPython internal; guard similarly
    try:
        import _winapi  # noqa: F401

        result["_winapi"] = True
    except ImportError:
        result["_winapi"] = False
    return result


def get_platform_helper() -> PlatformSupport:
    posix_info = _try_posix_imports()
    windows_info = _try_windows_imports()
    return PlatformSupport(
        is_posix=os.name == "posix",
        is_windows=os.name == "nt",
        posix_available=any(posix_info.values()),
        windows_available=any(windows_info.values()),
    )


def posix_file_lock(path: str) -> dict[str, object]:
    """POSIX file locking wrapper; explicit unsupported path on Windows."""
    if os.name != "posix":
        raise UnsupportedPlatformError("posix_file_lock is POSIX-only")
    try:
        import fcntl

        with open(path, "a", encoding="utf-8") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(fh, fcntl.LOCK_UN)
        return {"locked": True, "path": path}
    except OSError as exc:
        return {"locked": False, "error": str(exc)}


def windows_registry_probe(key: str = r"SOFTWARE\PortabilityLayer") -> dict[str, object]:
    """Windows registry wrapper; explicit unsupported path on POSIX.

    Guarded so the file parses on Linux; call raises on non-Windows.
    """
    if os.name != "nt":
        raise UnsupportedPlatformError("windows_registry_probe is Windows-only")
    # This branch is not executed on Linux, but must parse.
    try:
        import winreg  # type: ignore[import-not-found]

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as handle:  # type: ignore[attr-defined]
            value, _ = winreg.QueryValueEx(handle, "Probe")  # type: ignore[attr-defined]
            return {"value": value}
    except OSError as exc:
        return {"error": str(exc)}


def shared_wrapper(action: str, **kwargs: object) -> dict[str, object]:
    """One shared public wrapper dispatching to platform-specific helpers.

    Demonstrates feature detection versus platform-name branching.
    Callers use this single entry point; platform branches are internal.
    """
    support = get_platform_helper()
    if action == "lock":
        if support.is_posix:
            path = str(kwargs.get("path", "/tmp/portability-layer.lock"))
            return posix_file_lock(path)
        raise UnsupportedPlatformError(f"lock not supported on {sys.platform}")
    if action == "registry":
        if support.is_windows:
            return windows_registry_probe(str(kwargs.get("key", r"SOFTWARE\PortabilityLayer")))
        raise UnsupportedPlatformError(f"registry not supported on {sys.platform}")
    if action == "probe":
        return {
            "support": support,
            "posix_imports": _try_posix_imports(),
            "windows_imports": _try_windows_imports(),
        }
    raise UnsupportedPlatformError(f"unknown action {action!r}")


def demonstrate_fallbacks() -> dict[str, object]:
    support = get_platform_helper()
    # Feature-detection branch (import success) versus platform name
    try:
        result = shared_wrapper("probe")
        probe_ok = True
    except UnsupportedPlatformError:
        result = {}
        probe_ok = False
    # Explicit unsupported path demonstration
    unsupported_msg: str | None = None
    try:
        if support.is_posix:
            windows_registry_probe()
        else:
            posix_file_lock("/tmp/probe.lock")
    except UnsupportedPlatformError as exc:
        unsupported_msg = str(exc)
    return {
        "support": support,
        "probe": result,
        "probe_ok": probe_ok,
        "unsupported_path_message": unsupported_msg,
    }
