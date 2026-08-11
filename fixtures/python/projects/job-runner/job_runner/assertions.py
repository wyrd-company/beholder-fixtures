"""Assertions and optimization (PY-CAN-FLOW-006).

This module is executed under normal, -O, and -OO via child-process context.
"""

from __future__ import annotations

_side_effect_counter = 0


def side_effect_increment() -> bool:
    """Return True with observable side effect."""
    global _side_effect_counter
    _side_effect_counter += 1
    return True


def reset_counter() -> None:
    global _side_effect_counter
    _side_effect_counter = 0


def current_counter() -> int:
    return _side_effect_counter


def side_effectful_assertion(value: int) -> str:
    """Assert with side effect — removed under -O."""
    # Under python -O, this assert statement is removed entirely and
    # side_effect_increment is not called.
    assert side_effect_increment(), "side effect in assert"
    if value < 0:
        # Narrowing-style assert: proves value is non-negative past this point,
        # but must not be relied on as required control flow under -O.
        assert value >= 0, "value must be non-negative"
        # Under -O, the above assert is gone; code must handle negative via explicit check.
        if value < 0:
            return "handled-negatively-without-assert"
    return f"ok-{value}-counter-{_side_effect_counter}"


def debug_branch(enabled: bool = True) -> str:
    """Branch on __debug__ — stripped under -O."""
    if __debug__:
        return f"debug-enabled-{enabled}"
    return "debug-disabled-optimized"


def narrowing_but_unsafe_control(value: object) -> str:
    """Assertion used for narrowing is unsafe as required control flow.

    Static narrowing may assume value is str after assert, but at runtime
    under -O the check vanishes and later code must not rely on it.
    """
    assert isinstance(value, str), "expected str"
    # Correct control flow does not rely on assert:
    if not isinstance(value, str):
        return "fallback-non-string"
    # Now safe to treat as str regardless of optimization
    return f"string-{value.upper()}"  # type: ignore[union-attr]


def docstring_presence() -> str:
    """Return whether module docstring is present (removed under -OO)."""
    # Function docstring
    func_doc = side_effectful_assertion.__doc__
    mod_doc = __doc__
    return f"func-doc-{func_doc is not None}-mod-doc-{mod_doc is not None}"


def removed_assertion_observation() -> dict[str, object]:
    """Observable difference between normal and optimized runs."""
    reset_counter()
    # This assert will increment counter only in normal mode
    assert side_effect_increment()
    count_after_assert = current_counter()
    # __debug__ is False under -O/-OO
    return {
        "counter_after_assert": count_after_assert,
        "debug": __debug__,
        "doc_present": (__doc__ is not None),
    }
