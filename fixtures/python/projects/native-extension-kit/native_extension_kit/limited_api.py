"""PY-CAN-NATIVE-002: limited-API and stable vs version ABI."""

from __future__ import annotations

import sysconfig

try:
    from . import _native_limited  # type: ignore[import-not-found]
except ImportError:
    _native_limited = None  # type: ignore[assignment]

PY_LIMITED_API_MIN = 0x030A0000


def limited_api_demo() -> dict[str, object]:
    if _native_limited is None:
        return {"available": False, "reason": "limited extension not built"}
    return {
        "available": True,
        "hello": _native_limited.hello(),
        "add": _native_limited.add(2, 3),
        "limited_api_macro": hex(PY_LIMITED_API_MIN),
        "limited_api_macro_meaning": "Python 3.10 (Py_LIMITED_API 0x030A0000)",
        "stable_abi": True,
        "abi3_tag": "abi3",
        "version_tag_example": "cp314",
    }


def abi_tags_demo() -> dict[str, object]:
    soabi = sysconfig.get_config_var("SOABI") or ""
    ext_suffix = sysconfig.get_config_var("EXT_SUFFIX") or ""
    platform = sysconfig.get_platform()
    return {
        "soabi": soabi,
        "ext_suffix": ext_suffix,
        "platform": platform,
        "limited": "abi3",
        "version_specific": "cpython-314-x86_64-linux-gnu",
        "symbol_limit": "Limited API restricts to Py_LIMITED_API symbols; internal structs unavailable",
        "minimum_macro": hex(PY_LIMITED_API_MIN),
        "unavailable_apis": ["PyLongObject internals", "PyUnicode internal buffers", "Py_TYPE direct mutation"],
        "third_party_native_dependency": "none",
        "free_threaded_incompatibility": "abi3 extensions are not compatible with free-threaded (Py_GIL_DISABLED) builds without rebuild",
    }


__all__ = ["limited_api_demo", "abi_tags_demo", "PY_LIMITED_API_MIN"]
