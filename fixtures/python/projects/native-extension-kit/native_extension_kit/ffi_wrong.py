"""PY-CAN-NATIVE-005 isolated deliberately-wrong declaration.

This module isolates a deliberately wrong ctypes declaration because it can crash.
It is never imported for side effects; callers must explicitly invoke the demo
in an isolated subprocess.
"""

from __future__ import annotations

import ctypes
import pathlib
import subprocess
import sys

LIB_NAME = "libnative_kit.so"
_lib_path = pathlib.Path(__file__).with_name(LIB_NAME)


def wrong_declaration_demo_isolated() -> dict[str, object]:
    """Run wrong declaration in a subprocess to avoid crashing the parent."""
    code = f"""
import ctypes, pathlib
lib_path = pathlib.Path({str(_lib_path)!r})
lib = ctypes.CDLL(str(lib_path))
# Deliberately wrong: add_ints expects c_int, c_int but we declare c_char_p, c_char_p
lib.add_ints.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.add_ints.restype = ctypes.c_int
try:
    # Passing ints where char* expected is unsafe; we pass bytes to avoid immediate segfault
    # but width/convention mismatch still demonstrates wrong declaration.
    result = lib.add_ints(b"hi", b"there")
    print(f"wrong_result={{result}}")
except Exception as exc:
    print(f"exception={{type(exc).__name__}}:{{exc}}")
"""
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=5)
    return {
        "isolated": True,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "returncode": proc.returncode,
        "note": "Wrong declaration (width/calling convention) can crash; isolation via subprocess",
        "wrong_argtypes": "c_char_p instead of c_int",
    }


def describe_wrong_declaration() -> dict[str, str]:
    return {
        "wrong": "lib.add_ints.argtypes = [c_char_p, c_char_p] instead of [c_int, c_int]",
        "consequence": "stack corruption / segfault possible",
        "isolation": "subprocess via subprocess.run(sys.executable, ...)",
        "calling_convention": "CDLL vs WinDLL mismatch would also be wrong on Windows",
        "library_symbol": "symbol name libnative_kit.so / add_ints must match exactly",
    }


__all__ = ["wrong_declaration_demo_isolated", "describe_wrong_declaration"]
