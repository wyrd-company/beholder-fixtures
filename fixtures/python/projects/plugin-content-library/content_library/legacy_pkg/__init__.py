"""Legacy and mutable namespace path (PY-CAN-MOD-004).

Originally ``pkgutil.extend_path`` would extend ``__path__`` by scanning
``sys.path`` for matching subdirectories.  On Python 3.14 the finder-based
implementation queries the *parent* package's ``__path__`` finders for
subpackages, so a plain ``extend_path`` call for a subpackage does not
automatically discover ``sys.path`` entries.  This module demonstrates both
mechanisms:

- ``__path__`` mutation via ``extend_path`` (legacy contract, still
  documented for top-level packages)
- controlled ``__path__`` append (the shape that remains reliable for
  subpackages in modern Python)

The ``extra_plugin`` child lives in ``legacy_extra/content_library/legacy_pkg/``
and is found after the controlled mutation.
"""

from __future__ import annotations

from pkgutil import extend_path
import pathlib
import sys

# Legacy contract — retains the original call for graph coverage.
__path__ = extend_path(__path__, __name__)  # type: ignore

# Controlled mutation that actually extends the subpackage search path on
# Python 3.14+: locate the extra directory and append it.
_project_root = pathlib.Path(__file__).parent.parent.parent
_extra_candidate = _project_root / "legacy_extra" / "content_library" / "legacy_pkg"
if _extra_candidate.is_dir():
    candidate_str = str(_extra_candidate)
    if candidate_str not in __path__:
        __path__.append(candidate_str)

# Also support insertion via ``sys.path`` + ``site.addsitedir`` style:
# if the extra directory's parent is on ``sys.path`` we already appended.
# ``importlib.invalidate_caches()`` is required after path changes.

__all__ = ["__path__"]
