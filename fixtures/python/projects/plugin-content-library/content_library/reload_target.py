"""Reload target module (PY-CAN-MOD-019).

Re-executed by :func:`importlib.reload` to demonstrate reload semantics:
module identity is retained, new definitions replace old ones, stale aliases
and instances still reference old objects, removed names remain in old
references, extension reload note, and non-recursive dependency reload.

Source-state selection: editing this file between reloads changes which
definition is active.
"""

from __future__ import annotations

VERSION = 1
RETAINED_MARKER = "original"

def get_version() -> int:
    return VERSION

class Holder:
    """Instances capture the class object at creation time."""

    kind = "holder-v1"

    def describe(self) -> str:
        return f"holder-{VERSION}"

OLD_NAME = "will-be-removed-after-edit"
