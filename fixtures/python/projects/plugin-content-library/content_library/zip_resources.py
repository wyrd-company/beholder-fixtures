"""Zip import and package resources (PY-CAN-MOD-018).

Imports pure Python from an archive and reads data with
``importlib.resources``. Covers native-extension failure, namespace-resource
reader, fragile ``__file__`` resource access, and resource extraction.

The archive ``dist/content_pkg.zip`` is built by ``task build`` from
``zip_src/content_pkg`` and also contains an implicit namespace zip
``dist/shared_ns_portion.zip`` built from ``zip_ns_src/shared_ns``.
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
    """Read package resource from the zip-imported package (non-filesystem)."""
    project = pathlib.Path(__file__).parent.parent
    zip_path = project / "dist" / "content_pkg.zip"
    if not zip_path.exists():
        return {"note": "zip not yet built — run task build"}
    sys.path.insert(0, str(zip_path))
    for name in list(sys.modules):
        if name.startswith("content_pkg"):
            del sys.modules[name]
    import importlib

    importlib.invalidate_caches()
    try:
        pkg = importlib.import_module("content_pkg")
        # importlib.resources works for zip: files() returns a reader that can traverse the archive.
        text = importlib.resources.files(pkg).joinpath("data.txt").read_text(encoding="utf-8")
        # Demonstrate fragile ``__file__`` access vs resources API: __file__ points inside zip (e.g. ...zip/content_pkg/__init__.pyc)
        fragile_origin = getattr(pkg, "__file__", None)
        # Extraction via ``as_file`` for consumers needing a filesystem path.
        resource = importlib.resources.files(pkg).joinpath("data.txt")
        with importlib.resources.as_file(resource) as extracted:
            extracted_text = extracted.read_text(encoding="utf-8")
            extracted_exists = extracted.exists()
        return {
            "resources_text": text,
            "fragile_file": str(fragile_origin),
            "fragile_points_inside_zip": ".zip" in str(fragile_origin),
            "extracted_text": extracted_text,
            "extracted_exists": extracted_exists,
            "reader_type": type(importlib.resources.files(pkg)).__name__,
            "is_zip": True,
        }
    finally:
        if str(zip_path) in sys.path:
            sys.path.remove(str(zip_path))
        for name in list(sys.modules):
            if name.startswith("content_pkg"):
                del sys.modules[name]
        importlib.invalidate_caches()


def native_extension_zip_failure_demo() -> dict[str, object]:
    """Attempt to load a native extension from a zip archive — must fail (PY-CAN-MOD-018)."""
    import importlib
    import tempfile
    import zipfile

    project = pathlib.Path(__file__).parent.parent
    # Locate compiled extension to copy into a temporary zip.
    import sysconfig

    suffix = sysconfig.get_config_var("EXT_SUFFIX")
    ext_path = next(project.glob(f"content_library/_native_ext*{suffix}"), None)
    if ext_path is None:
        # Fallback: already built dist version may not exist, use source path.
        return {"note": "extension not built — run task build"}

    with tempfile.TemporaryDirectory() as tmp:
        zip_path = pathlib.Path(tmp) / "native_attempt.zip"
        with zipfile.ZipFile(str(zip_path), mode="w") as z:
            z.write(str(ext_path), f"native_pkg/_native_ext{suffix}")
            # Add an __init__.py so native_pkg is a package inside zip.
            z.writestr("native_pkg/__init__.py", "# pkg\n")
        sys.path.insert(0, str(zip_path))
        importlib.invalidate_caches()
        try:
            try:
                importlib.import_module("native_pkg._native_ext")
                return {"unexpected": "native extension loaded from zip should have failed"}
            except ImportError as exc:
                return {"native_extension_zip_failed": True, "error": str(exc), "error_type": exc.__class__.__name__}
        finally:
            if str(zip_path) in sys.path:
                sys.path.remove(str(zip_path))
            for name in list(sys.modules):
                if name.startswith("native_pkg"):
                    del sys.modules[name]
            importlib.invalidate_caches()


def namespace_resource_reader_demo() -> dict[str, object]:
    """Namespace-resource reader aggregates across __path__ entries (PY-CAN-MOD-018)."""
    project = pathlib.Path(__file__).parent.parent
    alpha = str(project / "ns_alpha")
    beta = str(project / "ns_beta")
    zip_ns = str(project / "dist" / "shared_ns_portion.zip")
    for p in (alpha, beta):
        if p not in sys.path:
            sys.path.insert(0, p)
    sys.path.insert(0, zip_ns)
    for name in list(sys.modules):
        if name.startswith("shared_ns"):
            del sys.modules[name]
    import importlib

    importlib.invalidate_caches()
    try:
        pkg = importlib.import_module("shared_ns")
        # For namespace packages, importlib.resources.files reads aggregated resources.
        # Each portion contributes its own data file; we read one via the resource API.
        reader_type = type(importlib.resources.files(pkg)).__name__
        # Try reading a resource that exists only in one portion — the multiplexer should still find it.
        # Use data_alpha.txt from alpha portion.
        try:
            alpha_text = importlib.resources.files(pkg).joinpath("data_alpha.txt").read_text(encoding="utf-8")
        except FileNotFoundError:
            alpha_text = "not-found"
        try:
            zip_text = importlib.resources.files(pkg).joinpath("data_zip.txt").read_text(encoding="utf-8")
        except FileNotFoundError:
            zip_text = "not-found"
        # List resources via contents traversal.
        is_namespace = getattr(pkg.__spec__, "submodule_search_locations", None) is not None
        return {
            "is_namespace": is_namespace,
            "reader_type": reader_type,
            "alpha_resource": alpha_text,
            "zip_resource": zip_text,
            "path_entries": [str(p) for p in getattr(pkg, "__path__", [])],
        }
    finally:
        for p in (alpha, beta, zip_ns):
            if p in sys.path:
                sys.path.remove(p)
        for name in list(sys.modules):
            if name.startswith("shared_ns"):
                del sys.modules[name]
        importlib.invalidate_caches()


def native_extension_zip_failure_note() -> str:
    return native_extension_zip_failure_demo().get("error", "native extensions cannot be loaded from zip archives — ImportError")  # type: ignore


def namespace_resource_reader_note() -> str:
    return str(namespace_resource_reader_demo().get("alpha_resource"))
