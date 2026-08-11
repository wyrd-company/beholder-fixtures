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

import importlib.abc
import importlib.machinery
import importlib.util
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
    """Create a spec with ``loader=None`` and show that import fails gracefully."""
    spec = importlib.machinery.ModuleSpec("synthetic_plugin.malformed", None, origin="synthetic://malformed")
    try:
        mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        return f"unexpected:{mod}"
    except (ValueError, ImportError) as exc:
        return f"malformed-spec:{exc.__class__.__name__}"


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
