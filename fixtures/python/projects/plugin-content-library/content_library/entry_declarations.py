"""Declaration-bearing source for script/module/__main__ identity (PY-CAN-MOD-001).

This module contains importable declarations (class, function, constant) and
exposes module identity metadata. It is exercised in four launching forms:

- ``import content_library.entry_declarations``
- ``python fixtures/python/projects/plugin-content-library/content_library/entry_declarations.py``
- ``python -m content_library.entry_declarations``
- ``python -m content_library`` (via ``content_library/__main__.py``)

Additional variants demonstrated here and in sibling modules:

- ``__name__ == "__main__"`` main guard
- duplicate module/class identities (same file under two import names)
- relative-import failure by direct execution (see ``relative_failure_demo``)
- ``runpy`` entry (see ``runpy_demo.py``)
- zip-application entry (see ``dist/library_app.pyz`` built by ``task build``)
"""

from __future__ import annotations

import sys

MODULE_LABEL = "entry-declarations"
MODULE_ORIGIN = __file__
MODULE_PACKAGE = __package__
MODULE_SPEC_NAME = getattr(__spec__, "name", None) if "__spec__" in globals() else None


class ContentItem:
    """Value object used to show duplicate class identities."""

    def __init__(self, label: str, kind: str = "generic") -> None:
        self.label = label
        self.kind = kind

    def describe(self) -> str:
        return f"{self.kind}:{self.label}"

    def __repr__(self) -> str:
        return f"ContentItem(label={self.label!r}, kind={self.kind!r})"


def create_item(label: str, kind: str = "generic") -> ContentItem:
    return ContentItem(label, kind)


def module_identity() -> dict[str, object]:
    """Return import-system identity for assertions by callers."""
    return {
        "name": __name__,
        "package": __package__,
        "spec_name": MODULE_SPEC_NAME,
        "file": __file__,
        "label": MODULE_LABEL,
    }


def relative_failure_demo() -> str:
    """Attempt a relative import that fails when executed as a script.

    When this file is run via ``python path/to/entry_declarations.py``
    ``__package__`` is ``None``/``""``, so ``from . import registry``
    raises ``ImportError``.  The helper captures that diagnostic for
    graph-level ``relative-import failure by direct execution`` coverage.
    """
    try:
        from . import registry  # type: ignore[attr-defined]  # noqa: F401

        return "relative-import-succeeded"
    except ImportError as exc:
        return f"relative-import-failed:{exc.__class__.__name__}"
    except Exception as exc:  # pragma: no cover
        return f"other-failure:{exc.__class__.__name__}"


def duplicate_identity_demo() -> dict[str, object]:
    """Load the same source file under two module names to show dual identities.

    Child-process variant is preferred, but an inline check demonstrates the
    shape: importing the same path-derived module under an alternate name
    creates a second module object and a second class object.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "content_library.entry_declarations_dup",
        __file__,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    same_class = module.ContentItem is ContentItem
    same_module = module is sys.modules[__name__]
    # Clean up the duplicate to avoid polluting later imports.
    del sys.modules[spec.name]
    return {
        "same_module": same_module,
        "same_class": same_class,
        "duplicate_name": spec.name,
    }


# Main guard — executed only when run as a script or ``-m`` entry point.
if __name__ == "__main__":
    ident = module_identity()
    print(f"running as __main__: {ident}")
    print(relative_failure_demo())
    # Exit used by launcher/child-process tests to distinguish script vs import.
    sys.exit(0)
