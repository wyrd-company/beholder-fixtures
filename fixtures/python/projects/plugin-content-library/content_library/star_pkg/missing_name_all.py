"""``__all__`` referencing a missing name (PY-CAN-MOD-008)."""

exists = "present"
__all__ = ["exists", "missing"]
# ``missing`` is not defined — ``from .missing_name_all import *`` will raise.
