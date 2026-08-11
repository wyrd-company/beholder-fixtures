"""PKG-013 runtime metadata and version lookup helpers."""

from __future__ import annotations

import importlib.metadata as meta
import pathlib


def query_distribution_files(dist: str = "distributable-suite-core") -> list[str]:
    try:
        files = meta.files(dist)
        return [str(f) for f in files] if files else []
    except meta.PackageNotFoundError:
        return []


def query_requires(dist: str = "distributable-suite-core") -> list[str]:
    try:
        return list(meta.distribution(dist).requires or [])
    except meta.PackageNotFoundError:
        return []


def query_entry_points_for_dist(dist: str = "distributable-suite-core") -> list[str]:
    try:
        d = meta.distribution(dist)
        return [f"{ep.name}={ep.value}" for ep in (d.entry_points or [])]
    except meta.PackageNotFoundError:
        return []


def source_tree_fallback() -> str:
    """When not installed, fallback to source tree attribute."""
    from suite_core import __version__

    return __version__


def distribution_import_mismatch_note() -> str:
    return "distribution distributable-suite-core provides imports suite_core, suite_core_utils, suite_shared_ns — reverse mapping is heuristic"
