"""Initializer failure for PY-CAN-MOD-002 — raises on import after partial state."""

partial_marker = "before-failure"
raise RuntimeError("failing package initializer")
