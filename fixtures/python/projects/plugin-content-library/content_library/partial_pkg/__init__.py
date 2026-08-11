"""Partially initialized package observation (PY-CAN-MOD-005).

During this ``__init__.py`` execution the package is already in
``sys.modules`` but ``CHILD_DONE`` not yet set.  The child observes this.
"""

import sys

# Record that we are inside __init__: module present but CHILD_DONE missing.
observed_module = sys.modules[__name__]
PARTIALLY_DURING_INIT = observed_module.__dict__.get("CHILD_DONE") is None

from . import child as _child  # noqa: F401

CHILD_DONE = True
OBSERVED_CHILD_VALUE = _child.VALUE
__all__ = ["PARTIALLY_DURING_INIT", "CHILD_DONE", "OBSERVED_CHILD_VALUE"]
