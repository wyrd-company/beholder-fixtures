"""Typed optional native accelerator fallback (PY-CAN-INT-008).

Select native or pure implementation through narrow handling and expose one typed public facade.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

# Marker for which impl was selected
ACCEL_IMPL: str
_fast_add_impl = None  # type: ignore[var-annotated]
_fast_multiply_impl = None  # type: ignore[var-annotated]

# Narrow handling: fallback only when the exact native module is absent, not for broken extension.
# ModuleNotFoundError with name == "feature_integration_suite._native_accel" means unsupported/missing wheel -> pure.
# Any other ImportError (missing symbol, broken init raising ImportError) must propagate to expose broken-extension variant.
try:
    from feature_integration_suite._native_accel import fast_add as _native_add  # type: ignore[import-not-found]
    from feature_integration_suite._native_accel import fast_multiply as _native_mul  # type: ignore[import-not-found]

    _fast_add_impl = _native_add
    _fast_multiply_impl = _native_mul
    ACCEL_IMPL = "native"
    _native_available = True
except ImportError as _exc:
    _missing_name = getattr(_exc, "name", None)
    # Only absent optional extension triggers fallback; present-but-broken must not be masked.
    if _missing_name not in (None, "feature_integration_suite._native_accel", "_native_accel"):
        # ImportError for a symbol or submodule other than the exact optional module -> broken extension
        raise
    if not isinstance(_exc, ModuleNotFoundError):
        # Pure ImportError (e.g., cannot import name) even with matching name should surface as broken
        # But allow fallback when the module file is truly absent (ModuleNotFoundError)
        # For safety, treat ImportError that is not ModuleNotFoundError as broken and re-raise
        raise
    # Unsupported wheel / missing compiled artifact falls back to pure
    from feature_integration_suite.pure_accel import fast_add as _pure_add
    from feature_integration_suite.pure_accel import fast_multiply as _pure_mul

    _fast_add_impl = _pure_add
    _fast_multiply_impl = _pure_mul
    ACCEL_IMPL = "pure"
    _native_available = False


# Typed public facade - single entry point regardless of impl
def fast_add(a: int, b: int) -> int:
    """Typed facade that dispatches to narrow-selected implementation."""
    return _fast_add_impl(a, b)  # type: ignore[no-any-return]


def fast_multiply(a: int, b: int) -> int:
    return _fast_multiply_impl(a, b)  # type: ignore[no-any-return]


def parity_check() -> dict[str, object]:
    """Verify parity drift: both impls produce same results for same inputs."""
    from feature_integration_suite import pure_accel

    cases = [(0, 0), (1, 2), (-5, 10), (100, 200)]
    mismatches: list[tuple[int, int, int, int]] = []
    for a, b in cases:
        pure = pure_accel.fast_add(a, b)
        facade = fast_add(a, b)
        if pure != facade:
            mismatches.append((a, b, pure, facade))
    return {"impl": ACCEL_IMPL, "mismatches": mismatches, "parity_ok": len(mismatches) == 0}


# Checker/runtime branch note: type checker sees stub's overloads, runtime follows narrow handling above.
# See accelerator.pyi for stub that declares fast_add/fast_multiply with type signatures.

broad_catch_would_mask_broken_extension = (
    "Narrow handling tests: `except ImportError` does not swallow RuntimeError from broken extension; "
    "`except Exception` would mask it"
)
unsupported_wheel_fallback = "When wheel incompatible or extension missing, pure fallback provides same typed facade"
