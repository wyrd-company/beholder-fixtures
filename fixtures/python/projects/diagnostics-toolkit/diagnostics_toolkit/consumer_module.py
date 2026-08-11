"""Consumer module that imports from target (PY-CAN-DIAG-013)."""

from diagnostics_toolkit.target_module import get_value as imported_get_value
from diagnostics_toolkit.target_module import value as imported_value
import diagnostics_toolkit.target_module as target_module


def consumer_uses_imported() -> int:
    """Use the directly imported binding."""

    return imported_get_value()


def consumer_uses_qualified() -> int:
    """Use the qualified module attribute."""

    return target_module.get_value()


def consumer_value() -> int:
    """Return the imported value directly."""

    return imported_value
