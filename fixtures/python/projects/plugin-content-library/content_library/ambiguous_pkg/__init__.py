"""``from package import name`` ambiguity (PY-CAN-MOD-007).

This package defines an attribute ``handler`` that shadows a child module
``handler.py``. ``from content_library.ambiguous_pkg import handler``
resolves to the attribute because the import system checks the package's
attributes before attempting a submodule fallback.
"""

from __future__ import annotations

# Package attribute that shadows the submodule name.
handler: str = "attribute-value"

# Also expose a value that does not shadow, to show fallback still works.
fallback_marker = "package-attr-exists"

# Cyclic timing note: during ``__init__`` execution the package is already in
# ``sys.modules``; a child that imported the package would see this partial
# state. See ``handler.py`` for the counterpart.
