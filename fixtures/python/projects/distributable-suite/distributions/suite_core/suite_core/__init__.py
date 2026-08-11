"""suite_core — flat-layout package."""

from __future__ import annotations

try:
    from ._generated_version import __version__
except ImportError:
    __version__ = "0.0.0.missing"

__all__ = ["__version__", "get_version", "PACKAGE_NAME"]

PACKAGE_NAME = "distributable-suite-core"
DISTRIBUTION_NAME = "distributable-suite-core"
IMPORT_NAMES = ["suite_core", "suite_core_utils"]


def get_version() -> str:
    return __version__


def is_flat_layout() -> bool:
    """Flat layout marker — packages live beside pyproject.toml."""
    return True
