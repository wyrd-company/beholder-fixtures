"""Circular import side B (PY-CAN-INT-003) - counterpart."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from feature_integration_suite.cycle_a import NodeA

from feature_integration_suite.cycle_a import NodeA as RuntimeNodeA  # runtime base import still required for some paths


class NodeB:
    """Peer node referencing NodeA."""

    prev_node: NodeA | None = None  # type: ignore[name-defined, valid-type]
    # Runtime annotation that will be evaluated eagerly if not stringized
    label: str = "b"

    def __init__(self, label: str) -> None:
        self.label = label
        self.prev_node = None

    def attach(self, other: NodeA) -> None:  # type: ignore[name-defined]
        self.prev_node = other


class HelperB:
    """Helper whose name is used as alias in cycle_a; demonstrates alias loss when namespace missing."""

    value: int = 99


class DecoratedBase(RuntimeNodeA):
    """Runtime base that requires actual import (cannot be TYPE_CHECKING-only)."""

    decorated_field: str = "decorated"


def decorated_factory() -> DecoratedBase:
    return DecoratedBase(value=1)


# Another decorator that requires runtime base evaluation
def runtime_base_decorator(func):  # type: ignore[no-untyped-def]
    return func


@runtime_base_decorator
def factory_needing_runtime_import() -> NodeB:
    # Must import NodeA at runtime for isinstance check
    from feature_integration_suite.cycle_a import NodeA

    node = NodeB(label="factory")
    return node
