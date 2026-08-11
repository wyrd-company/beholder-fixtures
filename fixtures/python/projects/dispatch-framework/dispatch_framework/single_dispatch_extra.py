"""Out-of-module singledispatch registration (PY-CAN-DYN-001)."""

from __future__ import annotations

from dispatch_framework.single_dispatch import format_value, out_of_module_handle

# Out-of-module registration requires import: this file imports the generic then registers.
format_value.register(list)(out_of_module_handle)
