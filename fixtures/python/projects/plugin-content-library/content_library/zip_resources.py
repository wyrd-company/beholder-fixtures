"""Zip import and package resources (PY-CAN-MOD-018).

Imports pure Python from an archive and reads data with
``importlib.resources``. Covers native-extension failure, namespace-resource
reader, fragile ``__file__`` resource access, and resource extraction.

The archive ``dist/content_pkg.zip`` is built by ``task build`` from
``zip_src/content_pkg``.  The same ``content_pkg/data.txt`` resource is also
available as a filesystem package for the ``importlib.resources`` reader demo.
"""

from __future__ import annotations

import pathlib
import sys
import importlib.resources
import importlib.util


def zip_import_demo() -> dict[str, object]:
    project = pathlib.Path(__file__).parent.parent
    zip_path = project / "dist" / "content_pkg.zip"
    if not zip_path.exists():
        return {"note": "zip not yet built — run task build"}
    sys.path.insert(0, str(zip_path))
    try:
        import importlib

        mod = importlib.import_module("content_pkg.zipped_module")
        return {
            "module": mod.__name__,
            "greet": mod.greet(),  # type: ignore
            "origin": getattr(mod.__spec__, "origin", None),
            "is_zip": ".zip" in str(getattr(mod.__spec__, "origin", "")),
        }
    finally:
        if str(zip_path) in sys.path:
            sys.path.remove(str(zip_path))
        for name in list(sys.modules):
            if name.startswith("content_pkg"):
                del sys.modules[name]


def resources_reader_demo() -> dict[str, object]:
    # ``importlib.resources.files`` works for both filesystem and zip loaders.
    # For the demo we read the filesystem copy in ``zip_src`` as a package
    # discovered via temporary path insertion, mirroring the zip-installed
    # portions note in MOD-003.
    import tempfile
    import shutil
    import importlib

    src_dir = pathlib.Path(__file__).parent.parent / "zip_src"
    sys.path.insert(0, str(src_dir))
    try:
        # Ensure content_pkg is importable from zip_src
        for name in list(sys.modules):
            if name.startswith("content_pkg"):
                del sys.modules[name]
        importlib.invalidate_caches()
        pkg = importlib.import_module("content_pkg")
        text = importlib.resources.files(pkg).joinpath("data.txt").read_text(encoding="utf-8")
        # Demonstrate fragile ``__file__`` access vs resources API.
        fragile = pathlib.Path(pkg.__file__).parent / "data.txt"  # type: ignore[arg-type]
        fragile_exists = fragile.exists()
        # Extraction via ``as_file`` for consumers needing a filesystem path.
        resource = importlib.resources.files(pkg).joinpath("data.txt")
        with importlib.resources.as_file(resource) as extracted:
            extracted_text = extracted.read_text(encoding="utf-8")
        return {
            "resources_text": text,
            "fragile_file_exists": fragile_exists,
            "extracted_text": extracted_text,
            "reader_type": type(importlib.resources.files(pkg)).__name__,
        }
    finally:
        if str(src_dir) in sys.path:
            sys.path.remove(str(src_dir))
        for name in list(sys.modules):
            if name.startswith("content_pkg"):
                del sys.modules[name]


def native_extension_zip_failure_note() -> str:
    return "native extensions cannot be loaded from zip archives — ImportError"


def namespace_resource_reader_note() -> str:
    return "implicit namespace packages require a resource reader that aggregates across __path__ entries"
