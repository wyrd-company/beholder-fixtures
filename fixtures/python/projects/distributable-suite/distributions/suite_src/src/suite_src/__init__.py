"""suite_src — src-layout package."""

from __future__ import annotations

from ._generated_version import __version__

__all__ = ["__version__", "get_version"]

PACKAGE_NAME = "distributable-suite-src"


def get_version() -> str:
    return __version__


def is_src_layout() -> bool:
    return True
