"""Architecture and build flags (PY-CAN-PLAT-010)."""

from __future__ import annotations

import struct
import sys
import sysconfig
from dataclasses import dataclass


@dataclass(frozen=True)
class BuildInfo:
    pointer_width_bits: int
    byteorder: str
    abiflags: str
    gil_disabled: int
    free_threaded: bool
    jit_enabled: bool
    debug_build: bool
    optimize_level: int
    optimized: bool
    version: str
    platform: str
    executable: str
    abi: str | None


def collect_build_info() -> BuildInfo:
    """Introspect pointer width, byte order, ABI and standard build flags."""
    pointer_width = struct.calcsize("P") * 8
    byteorder = sys.byteorder
    abiflags = getattr(sys, "abiflags", "") or ""
    # PEP 703 free-threaded and JIT flags — standard build actual (disabled).
    gil_disabled = int(sysconfig.get_config_var("Py_GIL_DISABLED") or 0)
    jit_val = sysconfig.get_config_var("Py_JIT")
    # Some builds expose _Py_JIT via sys._is_gil_enabled or sysconfig
    jit_enabled = bool(jit_val) if jit_val is not None else False
    # Debug build detection via Py_DEBUG or sysconfig
    py_debug = sysconfig.get_config_var("Py_DEBUG")
    debug_build = bool(py_debug)
    # Also check sys.flags.debug
    if sys.flags.debug:
        debug_build = True
    optimize_level = int(sys.flags.optimize)
    optimized = optimize_level > 0
    free_threaded = bool(gil_disabled)
    return BuildInfo(
        pointer_width_bits=pointer_width,
        byteorder=byteorder,
        abiflags=abiflags,
        gil_disabled=gil_disabled,
        free_threaded=free_threaded,
        jit_enabled=jit_enabled,
        debug_build=debug_build,
        optimize_level=optimize_level,
        optimized=optimized,
        version=sys.version,
        platform=sys.platform,
        executable=sys.executable,
        abi=sysconfig.get_config_var("SOABI"),
    )


def describe_pointer_width() -> dict[str, object]:
    width = struct.calcsize("P") * 8
    return {
        "pointer_width_bits": width,
        "is_64bit": width == 64,
        "is_32bit": width == 32,
        "maxsize": sys.maxsize,
    }


def describe_byteorder() -> dict[str, object]:
    return {
        "byteorder": sys.byteorder,
        "little_endian": sys.byteorder == "little",
        "struct_format": "<I" if sys.byteorder == "little" else ">I",
    }


def describe_abi() -> dict[str, object]:
    return {
        "abiflags": getattr(sys, "abiflags", ""),
        "soabi": sysconfig.get_config_var("SOABI"),
        "ext_suffix": sysconfig.get_config_var("EXT_SUFFIX"),
        "implementation": sys.implementation.name,
        "version": sys.implementation.version,
    }


def describe_build_flags() -> dict[str, object]:
    info = collect_build_info()
    return {
        "gil_disabled": info.gil_disabled,
        "free_threaded": info.free_threaded,
        "jit_enabled": info.jit_enabled,
        "debug_build": info.debug_build,
        "optimize_level": info.optimize_level,
        "optimized": info.optimized,
        "standard_build": not info.free_threaded and not info.jit_enabled and not info.debug_build and not info.optimized,
        "note": "Free-threaded and JIT flag values are the standard build's actual (disabled) flags per brief.",
    }


def optional_modules_probe() -> dict[str, bool]:
    """Probe optional stdlib modules availability."""
    import importlib.util

    candidates = ["_ctypes", "_ssl", "_tkinter", "zlib", "bz2", "lzma"]
    result: dict[str, bool] = {}
    for name in candidates:
        result[name] = importlib.util.find_spec(name) is not None
    return result


def demonstrate_build_info() -> dict[str, object]:
    info = collect_build_info()
    return {
        "info": info,
        "pointer": describe_pointer_width(),
        "byteorder": describe_byteorder(),
        "abi": describe_abi(),
        "flags": describe_build_flags(),
        "optional_modules": optional_modules_probe(),
    }
