"""Target module for mock patch lookup (PY-CAN-DIAG-013)."""

value = 42


def get_value() -> int:
    """Return the module-level value."""

    return value


def add(a: int, b: int) -> int:
    """Simple addition for autospec demonstration."""

    return a + b
