"""Delivery plugin registered across modules (PY-CAN-DYN-007)."""

from __future__ import annotations

from dispatch_framework.registries import HandlerMeta


class DeliveryPlugin(metaclass=HandlerMeta):
    channel = "delivery"
