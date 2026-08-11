"""Beta plugin that registers at import time (PY-CAN-MOD-012)."""

from content_library.registry import register_content

register_content("plugin-beta", {"kind": "beta"})

VALUE = "beta"
