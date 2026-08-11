"""Circular import side A (PY-CAN-INT-003) - breaks cycle via TYPE_CHECKING and stringized annotations."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from feature_integration_suite.cycle_b import NodeB  # only for type checkers, breaks runtime cycle
    from feature_integration_suite.cycle_b import HelperB as AliasedHelper  # alias variant


# Runtime base still needs real import for decorator / inheritance, but deferred via local import
def _get_node_b():  # local import cycle breaker
    from feature_integration_suite.cycle_b import NodeB

    return NodeB


class NodeA:
    """Node that references NodeB via forward annotation without importing at runtime."""

    # Eager vs stringized: on Python 3.14 annotations are deferred; this is stored as string/Deferred
    next_node: NodeB | None = None  # type: ignore[name-defined, valid-type]
    alias_field: AliasedHelper | None = None  # type: ignore[name-defined, valid-type]
    # Stringized forward ref via alias loss demonstration: bare string alias
    alias_loss_field: "HelperB | None" = None  # alias not imported at runtime, will fail without namespace

    def __init__(self, value: int) -> None:
        self.value = value

    def connect(self, other: NodeB) -> None:  # type: ignore[name-defined]
        self.next_node = other

    # Decorator still requires runtime import (cannot be broken statically)
    @staticmethod
    def create_with_decorator() -> NodeA:
        # local import ensures runtime base/decorator path still imports
        from feature_integration_suite.cycle_b import decorated_factory

        return decorated_factory()


# Early resolution failure: decorator attempts get_type_hints at class creation time before cycle resolved
def early_resolving_decorator(cls: type[object]) -> type[object]:
    import typing

    try:
        # Framework early resolution: evaluating hints now without full namespace should raise
        typing.get_type_hints(cls, include_extras=True)
        cls._early_resolved = True  # type: ignore[attr-defined]
    except Exception as exc:  # noqa: BLE001
        cls._early_resolution_error = str(exc)  # type: ignore[attr-defined]
        cls._early_resolved = False  # type: ignore[attr-defined]
    return cls


@early_resolving_decorator
class EarlyResolvedNode(NodeA):
    """Annotated with forward ref, decorated early before peer module fully loaded."""

    peer: NodeB | None = None  # type: ignore[name-defined]


def alias_loss_demo() -> str:
    """Alias `HelperB` imported only under TYPE_CHECKING; bare string \"HelperB\" fails without namespace."""
    import typing

    try:
        typing.get_type_hints(NodeA, include_extras=True)
        return "resolved-without-namespace-unexpected"
    except NameError as exc:
        return f"alias-loss-no-namespace:{exc.__class__.__name__}"
