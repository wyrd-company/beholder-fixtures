"""Catalog plugin registered across modules (PY-CAN-DYN-007)."""

from __future__ import annotations

from dispatch_framework.registries import PluginBase


class CatalogPlugin(PluginBase, plugin_name="catalog-cross"):
    channel = "catalog"
