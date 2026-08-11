"""Child that observes its parent partially initialized (PY-CAN-MOD-005)."""

import sys

parent = sys.modules["content_library.partial_pkg"]
# At import time, parent.CHILD_DONE not yet set — demonstrates partial init.
PARTIALLY_INITIALIZED = not hasattr(parent, "CHILD_DONE")
# Also show that parent is in sys.modules but not fully initialized.
PARENT_IN_SYS_MODULES = "content_library.partial_pkg" in sys.modules
VALUE = "partial-child-value"
