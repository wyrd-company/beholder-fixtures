"""suite_native_abi3 package: stable-ABI (abi3) native extension representative."""

from __future__ import annotations

try:
    from ._native_impl_abi3 import hello_abi3
except ImportError:
    hello_abi3 = None  # type: ignore

__all__ = ["hello_abi3"]
