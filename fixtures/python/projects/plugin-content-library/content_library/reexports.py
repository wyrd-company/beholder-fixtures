"""Additional re-export surface (PY-CAN-MOD-009).

Shows one object under several qualified bindings and public/private convention.
"""

from __future__ import annotations

from content_library._impl import InternalWidget
from content_library.facade import Widget  # noqa: F401

# One object, several names: InternalWidget (impl), Widget (facade), ReexportedWidget.
ReexportedWidget = InternalWidget

assert ReexportedWidget is InternalWidget

# Public vs private convention: underscore names are private, but still importable.
_public_name = "public-convention-example"
_private_name = "private-convention-example"

__all__ = ["ReexportedWidget", "Widget", "InternalWidget", "_public_name"]
