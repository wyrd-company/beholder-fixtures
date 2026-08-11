"""Alpha plugin that registers at import time (PY-CAN-MOD-012)."""

from content_library.registry import register_content

register_content("plugin-alpha", {"kind": "alpha"})

VALUE = "alpha"
