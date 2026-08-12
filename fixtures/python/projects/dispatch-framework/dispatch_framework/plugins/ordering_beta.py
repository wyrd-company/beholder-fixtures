"""Competing cross-module registration beta (PY-CAN-DYN-007 import-order)."""

from __future__ import annotations

from dispatch_framework.registries import PluginBase, register_handler


@register_handler("shared-key")
def handle_shared_beta(payload: object) -> str:
    return f"beta:{payload!r}"


class SharedPluginBeta(PluginBase, plugin_name="shared"):
    source = "beta"
