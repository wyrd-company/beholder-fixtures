"""Consumer that imports a target for patch-where-looked-up demo (PY-CAN-DYN-004)."""

from __future__ import annotations

from dispatch_framework.dotted_paths import produce_value as consumed_value


def consume_value() -> str:
    return consumed_value()
