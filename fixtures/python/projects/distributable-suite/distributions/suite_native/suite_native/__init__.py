"""suite_native package."""

from __future__ import annotations

try:
    from ._native_impl import hello as native_hello
except ImportError:
    native_hello = None  # type: ignore

__all__ = ["native_hello", "pure_fallback"]


def pure_fallback() -> str:
    return "pure-fallback"
