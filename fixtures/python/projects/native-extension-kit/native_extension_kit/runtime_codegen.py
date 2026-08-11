"""PY-CAN-NATIVE-007: runtime code generation variants."""

from __future__ import annotations

import ast
import pickle
import types
from typing import TYPE_CHECKING, Any, Callable, Protocol, runtime_checkable


@runtime_checkable
class AdderProtocol(Protocol):
    def __call__(self, value: int) -> int: ...


@runtime_checkable
class WidgetProtocol(Protocol):
    kind: str
    label: str


if TYPE_CHECKING:
    # Static stub surface: declarations a type checker would see for runtime-generated names
    adder_5: AdderProtocol
    adder_10: AdderProtocol
    StableWidget: type[WidgetProtocol]
    exec_add: Callable[[int, int], int]
    ast_mul: Callable[[int, int], int]


# Stable registry typed via protocols; runtime-generated values are consumed through it
registry: dict[str, AdderProtocol | type[WidgetProtocol] | Callable[..., Any]] = {}


def make_closure_adder(base: int) -> AdderProtocol:
    def adder(value: int) -> int:
        return value + base

    adder.__name__ = f"adder_{base}"
    adder.__qualname__ = f"adder_{base}"
    registry[adder.__name__] = adder  # type: ignore[assignment]
    return adder  # type: ignore[return-value]


def make_type_class(name: str, base: type | None = None) -> type[WidgetProtocol]:
    bases = (base,) if base is not None else (object,)
    attrs = {"kind": name.lower(), "label": name}
    cls = types.new_class(name, bases, {}, lambda ns: ns.update(attrs))
    alt = type(f"{name}Alt", bases, {"alt_kind": name.lower()})
    registry[name] = cls  # type: ignore[assignment]
    registry[alt.__name__] = alt  # type: ignore[assignment]
    return cls  # type: ignore[return-value]


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
    tree.body[0].args.args[0].arg = "a"
    code = compile(tree, "<synthetic-ast>", "exec")
    namespace: dict[str, Any] = {}
    exec(code, namespace)
    fn = namespace["ast_mul"]
    registry["ast_mul"] = fn
    return fn


def consume_via_protocol(name: str, value: int) -> int:
    obj = registry[name]
    if isinstance(obj, WidgetProtocol):
        raise TypeError("widget is not adder")
    # protocol check: AdderProtocol is callable
    assert isinstance(obj, AdderProtocol) or callable(obj)
    return obj(value)  # type: ignore[call-arg, operator]


def consume_widget_via_protocol(name: str) -> str:
    obj = registry[name]
    assert isinstance(obj, WidgetProtocol) or isinstance(obj, type)
    # access via protocol attributes
    return getattr(obj, "kind", str(obj))


def synthetic_traceback_demo() -> dict[str, object]:
    fn = make_exec_function()
    return {
        "filename": fn.__code__.co_filename,
        "qualname": fn.__qualname__,
        "module": fn.__module__,
        "traceback_contains_filename": "<synthetic-exec>" in fn.__code__.co_filename,
    }


def pickle_qualname_demo() -> dict[str, object]:
    fn = make_closure_adder(10)
    cls = make_type_class("RuntimeWidget")
    try:
        pickle.dumps(fn)
        fn_picklable = True
    except Exception as exc:
        fn_picklable = False
        fn_error = str(exc)
    else:
        fn_error = ""
    try:
        pickle.dumps(cls)
        cls_picklable = True
    except Exception as exc:
        cls_picklable = False
        cls_error = str(exc)
    else:
        cls_error = ""
    return {
        "function_qualname": fn.__qualname__,  # type: ignore[attr-defined]
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
        def f() -> int:
            return i

        funcs.append(f)
    shared = [f() for f in funcs]
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
    # demonstrate protocol consumption
    adder_result = consume_via_protocol("adder_5", 10)
    widget_kind = consume_widget_via_protocol("StableWidget")
    return {
        "registry_keys": sorted(registry.keys()),
        "protocol": "consume via stable registry/protocol",
        "adder_protocol_result": adder_result,
        "widget_protocol_kind": widget_kind,
    }


def stub_surface_demo() -> dict[str, object]:
    # Static stub surface exists in TYPE_CHECKING block above and via protocols;
    # runtime values conform to AdderProtocol/WidgetProtocol.
    fn = make_closure_adder(99)
    is_protocol = isinstance(fn, AdderProtocol)
    return {
        "has_protocol": True,
        "protocol_type": "AdderProtocol",
        "isinstance_check": is_protocol,
        "stub_declarations": ["adder_5", "adder_10", "StableWidget", "exec_add", "ast_mul"],
        "static_surface": "TYPE_CHECKING declares runtime names for checker",
    }


__all__ = [
    "AdderProtocol",
    "WidgetProtocol",
    "registry",
    "make_closure_adder",
    "make_type_class",
    "make_exec_function",
    "make_ast_function",
    "consume_via_protocol",
    "consume_widget_via_protocol",
    "synthetic_traceback_demo",
    "pickle_qualname_demo",
    "shared_cell_demo",
    "stable_registry_demo",
    "stub_surface_demo",
]
