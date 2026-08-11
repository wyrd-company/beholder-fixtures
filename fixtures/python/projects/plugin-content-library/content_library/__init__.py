"""Pluggable content library — regular package initialization (PY-CAN-MOD-002).

This package's ``__init__.py`` executes code on import, imports a child,
and re-exports a name. Co-located helper packages demonstrate the remaining
variants: empty versus side-effectful initializer, child attribute injection,
initializer failure, and partial state ordering.
"""

from __future__ import annotations

# Side-effectful initializer: executed at import time.
PACKAGE_INITIALIZED = True
PACKAGE_VERSION = "0.1.0"

# Child attribute injection: import a submodule and expose its name as a
# package attribute, mirroring the ``pkg.submodule`` attribute injection.
from . import registry as _registry  # noqa: F401
from .registry import CONTENT_REGISTRY, register_content

# Re-export a name from a child, the canonical ``__init__`` re-export pattern.
from .entry_declarations import ContentItem, create_item

# Also re-export a facade binding so star consumers see a single entry point.
from .facade import Widget as LibraryWidget  # noqa: F401

__all__ = [
    "CONTENT_REGISTRY",
    "ContentItem",
    "LibraryWidget",
    "PACKAGE_INITIALIZED",
    "PACKAGE_VERSION",
    "create_item",
    "register_content",
]

# Initializer ordering note: imports above run before this registry population.
register_content("library-root", {"source": "content_library.__init__"})

# Partial state demonstration: submodule ``failing_pkg`` raises on import.
# The failure is isolated; importing this package succeeds and leaves
# ``sys.modules['content_library']`` populated.  See
# ``content_library/failing_pkg/__init__.py``.
