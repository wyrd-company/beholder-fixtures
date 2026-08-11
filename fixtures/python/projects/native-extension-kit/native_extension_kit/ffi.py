"""PY-CAN-NATIVE-005: ctypes FFI variants against locally built native library."""

from __future__ import annotations

import ctypes
import ctypes.util
import pathlib

LIB_NAME = "libnative_kit.so"
_lib_path = pathlib.Path(__file__).with_name(LIB_NAME)

_lib = None
if _lib_path.exists():
    _lib = ctypes.CDLL(str(_lib_path))


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int)]
    _pack_ = 4


CALLBACK_T = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)


def _ensure_lib() -> ctypes.CDLL:
    if _lib is None:
        raise RuntimeError(f"native library not built: {_lib_path}")
    return _lib


def scalar_demo() -> dict[str, object]:
    lib = _ensure_lib()
    lib.add_ints.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.add_ints.restype = ctypes.c_int
    lib.scale_double.argtypes = [ctypes.c_double, ctypes.c_double]
    lib.scale_double.restype = ctypes.c_double
    return {
        "add_ints": lib.add_ints(7, 8),
        "scale_double": lib.scale_double(2.5, 4.0),
        "calling_convention": "CDLL (cdecl) on Linux x86_64",
        "width": "c_int 32-bit, c_double 64-bit",
    }


def struct_demo() -> dict[str, object]:
    lib = _ensure_lib()
    lib.make_point.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.make_point.restype = Point
    lib.point_sum.argtypes = [Point]
    lib.point_sum.restype = ctypes.c_int
    p = lib.make_point(3, 4)
    return {
        "point": {"x": p.x, "y": p.y},
        "sum": lib.point_sum(p),
        "packing": "explicit _pack_ = 4",
    }


def callback_demo() -> dict[str, object]:
    lib = _ensure_lib()
    lib.apply_callback.argtypes = [CALLBACK_T, ctypes.c_int]
    lib.apply_callback.restype = ctypes.c_int

    @CALLBACK_T
    def double_it(value: int) -> int:
        return value * 2

    # Keep reference to prevent GC while native holds pointer
    _keepalive = double_it
    result = lib.apply_callback(double_it, 21)
    return {"callback_result": result, "lifetime": "CFUNCTYPE must be kept alive while native may call it"}


def error_result_demo() -> dict[str, object]:
    lib = _ensure_lib()
    lib.divide_checked.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.divide_checked.restype = ctypes.c_int
    lib.get_last_error.argtypes = []
    lib.get_last_error.restype = ctypes.c_int
    lib.clear_last_error.argtypes = []
    lib.clear_last_error.restype = None

    lib.clear_last_error()
    ok = lib.divide_checked(10, 2)
    err_ok = lib.get_last_error()
    zero = lib.divide_checked(10, 0)
    err_zero = lib.get_last_error()
    return {
        "divide_ok": ok,
        "error_after_ok": err_ok,
        "divide_by_zero": zero,
        "error_after_zero": err_zero,
        "thread_local": "last_error is __thread thread-local",
    }


def library_resolution_demo() -> dict[str, object]:
    return {
        "library_path": str(_lib_path),
        "exists": _lib_path.exists(),
        "symbol_lookup": "CDLL + argtypes/restype explicit declarations",
        "packing_note": "Structure packing set via _pack_",
    }


__all__ = [
    "Point",
    "scalar_demo",
    "struct_demo",
    "callback_demo",
    "error_result_demo",
    "library_resolution_demo",
]
