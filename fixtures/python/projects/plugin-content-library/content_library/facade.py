"""Re-export and facade bindings (PY-CAN-MOD-009).

Re-exports private implementation and third-party names through facade
modules. Demonstrates redundant alias for typing, one object under several
qualified bindings, public/private convention, and drift between runtime
and stub.
"""

from __future__ import annotations

# Re-export private implementation under a public name.
from content_library._impl import InternalWidget as Widget
from content_library._impl import PUBLIC_CONSTANT, _private_helper  # noqa: F401

# Redundant alias for typing: both ``Widget`` and ``InternalWidget`` refer to same object.
InternalWidget = Widget

# Third-party (stdlib) re-export through the facade.
from pathlib import Path as ContentPath
from json import dumps as content_dumps  # noqa: F401

# Facade also re-exports via its own alias so one object has several qualified names:
# - content_library._impl.InternalWidget
# - content_library.facade.Widget
# - content_library.facade.InternalWidget
# - content_library.LibraryWidget (via package __init__)
# All are ``is`` identical.

__all__ = ["Widget", "InternalWidget", "ContentPath", "PUBLIC_CONSTANT"]

# Drift note: ``facade.pyi`` stub declares ``Widget`` as a protocol with an
# extra method ``extra_stub_only`` that does not exist at runtime, demonstrating
# drift between stub and implementation. See ``facade.pyi``.
