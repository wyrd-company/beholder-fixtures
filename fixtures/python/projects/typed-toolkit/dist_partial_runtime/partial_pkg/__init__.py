"""Runtime package for the partial-overlay pair.

This is the matching runtime distribution (``typed-toolkit-partial``) that the
separate ``typed-toolkit-partial-stubs`` overlay stubs only partially.  The
package ships its own ``py.typed`` marker so its inline types serve as the
fallback for the symbols the partial stub package does not cover.
"""

from __future__ import annotations

partial_value: int = 1


def partial_func(x: int) -> str:
    return str(x)


def only_runtime_typed(x: int) -> int:
    # Covered by inline runtime types; intentionally absent from the partial
    # stub overlay so the checker must fall back to this package.
    return x + 1
