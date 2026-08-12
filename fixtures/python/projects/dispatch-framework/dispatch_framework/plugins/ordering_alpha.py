"""Competing cross-module registration alpha (PY-CAN-DYN-007 import-order)."""

from __future__ import annotations

from dispatch_framework.registries import PluginBase, register_handler


@register_handler("shared-key")
def handle_shared_alpha(payload: object) -> str:
    return f"alpha:{payload!r}"


class SharedPluginAlpha(PluginBase, plugin_name="shared"):
    source = "alpha"
