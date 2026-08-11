"""Side-effectful initializer contrasting with empty_pkg (PY-CAN-MOD-002)."""

PACKAGE_MARKER = "initialized_pkg_init_ran"

from . import child as _child

reexported = _child.CHILD_VALUE
__all__ = ["PACKAGE_MARKER", "reexported"]
