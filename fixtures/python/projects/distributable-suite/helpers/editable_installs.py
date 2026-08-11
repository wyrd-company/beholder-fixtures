"""PKG-011 editable installs variants."""

from __future__ import annotations

# Editable install variants demonstrated via pip -e with setuptools backend:
# - Static .pth: setuptools writes a .pth pointing to source
# - Finder: PEP 660 finder-based editable (import hook)
# - Strict vs lenient: strict rebuilds metadata, lenient tolerates changes
# - Added package behavior: new packages after editable install may not appear until reinstall
# Contrast: metadata changes (pyproject version) need rebuild; source changes are immediate.

EDITABLE_COMMAND = "pip install --no-index --find-links wheelhouse -e distributions/suite_core"

FINDER_NOTE = "setuptools uses .pth fallback on this version; newer pip uses editable finder"


def source_change_without_reinstall_demo() -> str:
    return "edit suite_core/plugins.py, re-import without reinstall sees new value"


def metadata_needs_rebuild_note() -> str:
    return "changing pyproject version requires reinstall -e to update .dist-info"


def native_needs_rebuild_note() -> str:
    return "native extension changes need rebuild, not just source edit"


def entry_point_needs_rebuild_note() -> str:
    return "entry point table changes need rebuild to update console wrapper"


def path_provenance_note() -> str:
    return "editable .pth or finder reports origin as source tree via importlib.metadata.packages_distributions"
