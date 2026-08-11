"""Plugin package for registry discovery."""

from dispatch_framework.plugins.catalog_plugin import CatalogPlugin  # noqa: F401
from dispatch_framework.plugins.delivery_plugin import DeliveryPlugin  # noqa: F401

__all__ = ["CatalogPlugin", "DeliveryPlugin"]
