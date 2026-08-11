"""PY-CAN-NATIVE-007: runtime code generation variants."""

from __future__ import annotations

import ast
import pickle
import types
import traceback
from typing import Any, Callable


registry: dict[str, Any] = {}


def make_closure_adder(base: int) -> Callable[[int], int]:
    def adder(value: int) -> int:
        return value + base

    adder.__name__ = f"adder_{base}"
    adder.__qualname__ = f"adder_{base}"
    registry[adder.__name__] = adder
    return adder


def make_type_class(name: str, base: type | None = None) -> type:
    bases = (base,) if base is not None else (object,)
    attrs = {"kind": name.lower(), "label": name}
    cls = types.new_class(name, bases, {}, lambda ns: ns.update(attrs))
    # Alternative via type()
    alt = type(f"{name}Alt", bases, {"alt_kind": name.lower()})
    registry[name] = cls
    registry[alt.__name__] = alt
    return cls


def make_exec_function() -> Callable[[int, int], int]:
    source = "def exec_add(a, b):\n    return a + b\n"
    code = compile(source, "<synthetic-exec>", "exec")
    namespace: dict[str, Any] = {}
    exec(code, namespace)
    fn = namespace["exec_add"]
    fn.__module__ = __name__
    registry["exec_add"] = fn
    return fn


def make_ast_function() -> Callable[[int, int], int]:
    tree = ast.parse("def ast_mul(a, b): return a * b")
    # Synthetic filename affects traceback
    tree.body[0].args.args[0].arg = "a"  # keep deterministic
    code = compile(tree, "<synthetic-ast>", "exec")
    namespace: dict[str, Any] = {}
    exec(code, namespace)
    fn = namespace["ast_mul"]
    registry["ast_mul"] = fn
    return fn


def synthetic_traceback_demo() -> dict[str, object]:
    fn = make_exec_function()
    # Capture synthetic filename from code object
    return {
        "filename": fn.__code__.co_filename,
        "qualname": fn.__qualname__,
        "module": fn.__module__,
        "traceback_contains_filename": "<synthetic-exec>" in fn.__code__.co_filename,
    }


def pickle_qualname_demo() -> dict[str, object]:
    fn = make_closure_adder(10)
    cls = make_type_class("RuntimeWidget")
    # Functions created at runtime with module/qualname may not pickle unless importable
    try:
        pickle.dumps(fn)
        fn_picklable = True
    except Exception as exc:
        fn_picklable = False
        fn_error = str(exc)
    else:
        fn_error = ""
    # Class created via type() shares module
    try:
        pickle.dumps(cls)
        cls_picklable = True
    except Exception as exc:
        cls_picklable = False
        cls_error = str(exc)
    else:
        cls_error = ""
    return {
        "function_qualname": fn.__qualname__,
        "class_qualname": cls.__qualname__,
        "function_picklable": fn_picklable,
        "function_pickle_error": fn_error,
        "class_picklable": cls_picklable,
        "class_pickle_error": cls_error,
        "note": "module/qualname affect pickle; synthetic functions need importable path",
    }


def shared_cell_demo() -> dict[str, object]:
    funcs: list[Callable[[], int]] = []
    for i in range(3):
        # Accidental shared cell if closure captures loop variable without default
        def f() -> int:
            return i

        funcs.append(f)
    # All share final i == 2
    shared = [f() for f in funcs]
    # Correct via default argument
    corrected: list[Callable[[], int]] = []
    for i in range(3):
        def g(i=i) -> int:  # type: ignore[no-redef]
            return i

        corrected.append(g)
    isolated = [f() for f in corrected]
    return {"shared_cells": shared, "isolated_via_default": isolated}


def stable_registry_demo() -> dict[str, object]:
    make_closure_adder(5)
    make_type_class("StableWidget")
    make_exec_function()
    make_ast_function()
    return {"registry_keys": sorted(registry.keys()), "protocol": "consume via stable registry/protocol"}


def stub_surface_note() -> dict[str, str]:
    return {
        "stub": "Static stubs for runtime-generated symbols are intentionally absent; runtime surface is dynamic",
        "static_checker": "Type checker cannot see registry entries without stub generation",
    }


__all__ = [
    "registry",
    "make_closure_adder",
    "make_type_class",
    "make_exec_function",
    "make_ast_function",
    "synthetic_traceback_demo",
    "pickle_qualname_demo",
    "shared_cell_demo",
    "stable_registry_demo",
    "stub_surface_note",
]
