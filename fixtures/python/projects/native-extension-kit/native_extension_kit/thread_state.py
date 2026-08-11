"""PY-CAN-NATIVE-004: GIL release and reacquire around blocking work."""

from __future__ import annotations

import sysconfig
import time

try:
    from . import _native_single  # type: ignore[import-not-found]
except ImportError:
    _native_single = None  # type: ignore[assignment]


def blocking_work_demo(millis: int = 20) -> dict[str, object]:
    if _native_single is None:
        return {"available": False}
    start = time.monotonic()
    _native_single.blocking_work(millis)
    elapsed = time.monotonic() - start
    return {
        "available": True,
        "requested_ms": millis,
        "elapsed_s": elapsed,
        "gil": "released via Py_BEGIN_ALLOW_THREADS / Py_END_ALLOW_THREADS",
        "note": "Python API must not be called while detached; external thread would need PyGILState_Ensure",
    }


def gil_reacquire_demo() -> dict[str, object]:
    if _native_single is None:
        return {"available": False}
    result = _native_single.call_python_while_detached_error()
    return {
        "result": result,
        "mechanism": "Py_BEGIN_ALLOW_THREADS ... Py_END_ALLOW_THREADS then PyUnicode_FromString",
        "python_api_while_detached": "undefined behavior — must reacquire first",
        "external_thread": "native thread calling Python must use PyGILState_Ensure / PyGILState_Release",
        "subinterpreter": "excluded variant: high-level subinterpreter API unstable; not declared", 
        "free_threaded_excluded": "free-threaded declaration variant excluded; installed build is GIL-enabled",
        "gil_disabled": sysconfig.get_config_var("Py_GIL_DISABLED"),
        "incompatible_extension": "extension incompatible with free-threaded may re-enable GIL",
    }


__all__ = ["blocking_work_demo", "gil_reacquire_demo"]
