"""First-class functions, lambdas, nesting, and qualified identity (PY-CAN-CALL-004)."""

from __future__ import annotations

from typing import Callable


def named_handler(parcel: str) -> str:
    """A named function used for aliasing and reference edges."""

    return f"handled:{parcel}"


named_alias = named_handler
stored_handlers: list[Callable[[str], str]] = [named_handler, lambda parcel: f"lambda:{parcel}"]


def factory(label: str) -> Callable[[], str]:
    """Return a new nested function capturing its label; each call creates distinct objects."""

    tag = label

    def reader() -> str:
        return f"factory:{tag}"

    return reader


def lambda_identity() -> dict[str, str]:
    """Inspect ``<lambda>`` and ``<locals>`` qualified names."""

    inline = lambda parcel: f"inline:{parcel}"  # noqa: E731 — fixture lambda variant

    def outer():
        def inner() -> str:
            return inner.__qualname__

        return inner

    nested = outer()
    return {
        "lambda_name": inline.__name__,
        "lambda_qualname": inline.__qualname__,
        "locals_qualname": nested.__qualname__,
        "locals_name": nested.__name__,
    }


def rebinding_leaves_metadata() -> dict[str, object]:
    """Rebinding a function name does not alter previously created aliases."""

    def original(parcel: str) -> str:
        """Original doc."""

        return parcel

    alias = original

    def replacement(parcel: str) -> str:
        """Replacement doc."""

        return parcel.upper()

    # Rebind the module name; alias still points to original.
    original = replacement  # type: ignore[assignment]
    return {
        "alias_is_replacement": alias is replacement,
        "alias_name": alias.__name__,
        "alias_doc": alias.__doc__,
        "current_name": original.__name__,
    }


def distinct_factory_instances() -> bool:
    """Two calls to the factory produce distinct closure objects."""

    first = factory("alpha")
    second = factory("alpha")
    return first is not second and first() == second()


def reference_edge_vs_call_edge() -> dict[str, object]:
    """Distinguish a reference edge from a call edge and compare function identity."""

    handler_ref = named_handler
    result = handler_ref("parcel-1")
    same_ref = handler_ref is named_handler
    alias_ref = named_alias is named_handler
    stored_ref = stored_handlers[0] is named_handler
    return {
        "result": result,
        "same_ref": same_ref,
        "alias_ref": alias_ref,
        "stored_ref": stored_ref,
    }


def return_and_store_callbacks() -> list[Callable[[str], str]]:
    """Return and collect first-class callables."""

    callbacks: list[Callable[[str], str]] = []
    callbacks.append(named_handler)
    callbacks.append(lambda parcel: f"stored:{parcel}")  # noqa: E731
    callbacks.append(factory("stored-label"))
    return callbacks
