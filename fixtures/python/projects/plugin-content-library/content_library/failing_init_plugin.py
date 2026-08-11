"""Failing initializer for PY-CAN-MOD-012 — raises at import time."""

from content_library.registry import register_content

register_content("failing-init-before-raise", {"phase": "before-raise"})
raise RuntimeError("intentional initializer failure")
