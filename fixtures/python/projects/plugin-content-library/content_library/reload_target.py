"""Reload target module (PY-CAN-MOD-019).

Re-executed by :func:`importlib.reload` to demonstrate reload semantics:
module identity is retained, new definitions replace old ones, stale aliases
and instances still reference old objects, removed names remain in old
references, extension reload note, and non-recursive dependency reload.

Source-state selection: editing this file between reloads changes which
definition is active.
"""

from __future__ import annotations

import content_library.reload_dep as reload_dep  # dependency for non-recursive reload variant

VERSION = 1
RETAINED_MARKER = "original"
DEP_VALUE = reload_dep.DEP_VALUE

def get_version() -> int:
    return VERSION

def get_dep_value() -> str:
    return reload_dep.DEP_VALUE

class Holder:
    """Instances capture the class object at creation time."""

    kind = "holder-v1"

    def describe(self) -> str:
        return f"holder-{VERSION}"

OLD_NAME = "will-be-removed-after-edit"
