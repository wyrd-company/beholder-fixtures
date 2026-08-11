"""Finders, loaders, specs, and non-file modules (PY-CAN-MOD-015).

Implements a minimal meta-path finder/loader producing a synthetic module
with an explicit :class:`importlib.machinery.ModuleSpec` and custom ``origin``.

Covers:

- pre-existing module (finder defers if already in ``sys.modules``)
- malformed spec (missing loader)
- source, namespace, zip, frozen, extension, generated loader varieties
- ``.pth`` startup path (via ``site.addsitedir`` on ``pth_space``)
"""

from __future__ import annotations

import importlib
import importlib.abc
import importlib.machinery
import sys
import types


SYNTHETIC_NAME = "synthetic_plugin"
SYNTHETIC_ORIGIN = "synthetic://plugin-content-library/synthetic_plugin"


class SyntheticLoader(importlib.abc.Loader):
    """Loader that populates a synthetic non-file module."""

    def create_module(self, spec: importlib.machinery.ModuleSpec) -> types.ModuleType | None:
        return None  # use default module creation

    def exec_module(self, module: types.ModuleType) -> None:
        module.__dict__.update(
            {
                "SYNTHETIC": True,
                "origin": SYNTHETIC_ORIGIN,
                "value": "from-synthetic-loader",
            }
        )
        # Mark as non-file module without ``__file__`` via spec flag,
        # but keep ``__spec__`` for assertions.


class SyntheticFinder(importlib.abc.MetaPathFinder):
    """Meta-path finder that claims ``synthetic_plugin`` and sibling names."""

    CLAIMED = {SYNTHETIC_NAME, "synthetic_plugin.sub"}

    def find_spec(
        self,
        fullname: str,
        path: object,
        target: object = None,
    ) -> importlib.machinery.ModuleSpec | None:
        if fullname not in self.CLAIMED:
            return None
        if fullname in sys.modules:
            # Pre-existing module: do not claim, let normal cache win.
            return None
        if fullname == "synthetic_plugin.sub":
            # Malformed spec demo is handled by ``malformed_spec_demo``; here return valid child.
            return importlib.machinery.ModuleSpec(
                fullname,
                SyntheticLoader(),
                origin=f"{SYNTHETIC_ORIGIN}/sub",
                is_package=False,
            )
        return importlib.machinery.ModuleSpec(
            fullname,
            SyntheticLoader(),
            origin=SYNTHETIC_ORIGIN,
            is_package=False,
        )


_FINDER = SyntheticFinder()


def install_finder() -> None:
    if _FINDER not in sys.meta_path:
        sys.meta_path.insert(0, _FINDER)


def uninstall_finder() -> None:
    if _FINDER in sys.meta_path:
        sys.meta_path.remove(_FINDER)


def malformed_spec_demo() -> str:
    """Drive the import machinery with a genuinely malformed spec.

    A spec whose ``loader`` is ``None`` while it is *not* a namespace package
    (``submodule_search_locations`` is ``None``) is malformed.  The failure is
    not a loader that chooses to raise: the import machinery itself detects the
    missing loader in ``_bootstrap._load_unlocked`` and raises
    ``ImportError('missing loader')`` when it tries to load the module.  A
    temporary meta-path finder hands that malformed spec to the real import
    operation so the failure arises naturally from ``import_module``.  A
    top-level name is used so no parent-package resolution precedes the
    malformed spec.
    """

    name = "malformed_plugin"

    class MalformedSpecFinder(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path, target=None):  # type: ignore[override]
            if fullname != name:
                return None
            # loader=None with no submodule_search_locations => malformed spec.
            return importlib.machinery.ModuleSpec(fullname, None, origin="synthetic://malformed")

    finder = MalformedSpecFinder()
    sys.meta_path.insert(0, finder)
    try:
        mod = importlib.import_module(name)
        return f"unexpected:{mod!r}"
    except ImportError as exc:
        return f"malformed-spec:{exc.__class__.__name__}: {exc}"
    finally:
        if finder in sys.meta_path:
            sys.meta_path.remove(finder)
        sys.modules.pop(name, None)


def loader_varieties() -> dict[str, str]:
    """Return the loader class name for each conceptual loader variety."""
    # Each entry demonstrates which loader Python would assign for that
    # origin kind. Values are strings so the file remains importable without
    # constructing real frozen/zip artifacts.
    return {
        "source": "SourceFileLoader",
        "namespace": "_NamespacePath / None loader + ModuleSpec(is_package=True, loader=None)",
        "zip": "ZipImporter",
        "frozen": "FrozenImporter",
        "extension": "ExtensionFileLoader",
        "generated": "SourcelessFileLoader",
    }


def pth_startup_demo() -> str:
    """Simulate ``.pth`` startup code via ``site.addsitedir``.

    The project ships ``pth_space/demo.pth`` containing
    ``import content_library.finder_loader``.  ``site.addsitedir`` processes
    each ``.pth`` line, executing ``import`` lines as startup code.
    """
    import site
    import pathlib

    pth_dir = pathlib.Path(__file__).parent.parent / "pth_space"
    # ``addsitedir`` will read ``demo.pth`` and execute its import line.
    site.addsitedir(str(pth_dir))
    return f"pth-processed:{pth_dir / 'demo.pth'}"
