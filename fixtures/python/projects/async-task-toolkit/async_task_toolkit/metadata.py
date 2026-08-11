"""Function metadata and arbitrary attributes (PY-CAN-CALL-015)."""

from __future__ import annotations

import inspect
import subprocess
import sys
from types import FunctionType


def parcel_handler(label: str, priority: int = 1, *, mode: str = "standard") -> str:
    """Handle a parcel with priority and mode.

    This docstring is load-bearing for the ``-OO`` variant.
    """

    return f"{label}:{priority}:{mode}"


# User-set marker attribute.
parcel_handler.marker = "toolkit-marker"  # type: ignore[attr-defined]


def inspect_metadata() -> dict[str, object]:
    """Inspect canonical function metadata fields."""

    return {
        "name": parcel_handler.__name__,
        "qualname": parcel_handler.__qualname__,
        "module": parcel_handler.__module__,
        "doc": parcel_handler.__doc__,
        "defaults": parcel_handler.__defaults__,
        "kwdefaults": parcel_handler.__kwdefaults__,
        "annotations": parcel_handler.__annotations__,
        "closure": parcel_handler.__closure__,
        "code": parcel_handler.__code__.co_name,
        "marker": parcel_handler.marker,  # type: ignore[attr-defined]
    }


def signature_inspection() -> dict[str, object]:
    """Inspect the function's signature object."""

    sig = inspect.signature(parcel_handler)
    return {
        "parameters": list(sig.parameters.keys()),
        "text": str(sig),
        "return_annotation": sig.return_annotation,
    }


def wrapper_metadata_divergence() -> dict[str, object]:
    """Wrapping without ``functools.wraps`` leaves divergent metadata."""

    def bare_wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
        return parcel_handler(*args, **kwargs)

    import functools

    @functools.wraps(parcel_handler)
    def wrapped(*args, **kwargs):  # type: ignore[no-untyped-def]
        return parcel_handler(*args, **kwargs)

    return {
        "bare_name": bare_wrapper.__name__,
        "bare_wrapped": hasattr(bare_wrapper, "__wrapped__"),
        "wrapped_name": wrapped.__name__,
        "wrapped_has_wrapped": hasattr(wrapped, "__wrapped__"),
        "wrapped_doc": wrapped.__doc__,
    }


def rebinding_preserves_original() -> dict[str, object]:
    """Rebinding the name leaves the original object intact."""

    original = parcel_handler
    alias = original

    def replacement(label: str) -> str:
        """Replacement handler."""

        return label.upper()

    # Rebind local name; alias still points to original.
    handler = replacement  # noqa: F841
    return {
        "alias_is_original": alias is original,
        "alias_name": alias.__name__,
        "replacement_name": replacement.__name__,
    }


def synthetic_signature() -> dict[str, object]:
    """Expose a synthetic signature through callable metadata and resolve it."""

    params = [
        inspect.Parameter("label", inspect.Parameter.POSITIONAL_OR_KEYWORD),
        inspect.Parameter("priority", inspect.Parameter.KEYWORD_ONLY, default=1),
    ]
    synthetic = inspect.Signature(params, return_annotation=str)

    def target(label: str, priority: int = 1) -> str:
        return f"{label}:{priority}"

    target.__signature__ = synthetic  # type: ignore[attr-defined]
    resolved = inspect.signature(target)
    return {
        "synthetic": str(synthetic),
        "resolved": str(resolved),
        "matches": resolved == synthetic,
        "callable": target.__name__,
    }


def doc_removal_via_oo() -> dict[str, object]:
    """Run a child process with ``-OO`` to demonstrate docstring removal.

    Under ``-OO`` CPython strips docstrings, so ``__doc__`` becomes ``None``.
    This exercises the declared child-process / interpreter-flags context.
    """

    code = (
        "import async_task_toolkit.metadata as m;"
        "print(repr(m.parcel_handler.__doc__))"
    )
    default_out = subprocess.check_output([sys.executable, "-c", code], text=True).strip()
    oo_out = subprocess.check_output([sys.executable, "-OO", "-c", code], text=True).strip()
    return {
        "default_doc": default_out,
        "oo_doc": oo_out,
        "oo_is_none": oo_out == "None",
    }


def closure_inspection() -> dict[str, object]:
    """Inspect closure cells for a factory-created function."""

    def make_adder(base: int) -> FunctionType:
        offset = base

        def adder(value: int) -> int:
            return value + offset

        return adder

    adder = make_adder(10)
    return {
        "closure": adder.__closure__,
        "cell_contents": adder.__closure__[0].cell_contents if adder.__closure__ else None,
        "freevars": adder.__code__.co_freevars,
    }


def arbitrary_attribute_assignment() -> dict[str, object]:
    """Assign and read arbitrary attributes on functions."""

    def target(value: str) -> str:
        return value

    target.custom_flag = True  # type: ignore[attr-defined]
    target.counter = 42  # type: ignore[attr-defined]
    return {
        "flag": target.custom_flag,  # type: ignore[attr-defined]
        "counter": target.counter,  # type: ignore[attr-defined]
        "has_dict": hasattr(target, "__dict__"),
    }
