"""Doctest execution examples (PY-CAN-DIAG-014).

This module provides docstring and text examples with shared state,
exception output, and one option directive.
"""

from __future__ import annotations


def add(a: int, b: int) -> int:
    """Add two numbers.

    Shared state example:

    >>> counter = 0
    >>> counter += add(2, 3)
    >>> counter
    5
    >>> counter += add(1, 1)
    >>> counter
    7

    Simple truth:

    >>> add(2, 3)
    5
    """
    return a + b


def failing_func() -> int:
    """Always fails.

    Exception output:

    >>> failing_func()
    Traceback (most recent call last):
    ...
    ValueError: demo failure
    """
    raise ValueError("demo failure")


def long_list() -> list[int]:
    """Return a long list for ellipsis demonstration.

    Ellipsis directive:

    >>> long_list()  # doctest: +ELLIPSIS
    [1, 2, 3, ...]
    """
    return [1, 2, 3, 4, 5, 6]


def greet(name: str) -> str:
    """Greet someone.

    >>> greet("world")
    'hello world'
    """
    return f"hello {name}"


# Text file examples are also run via doctest.testfile on
# diagnostics_toolkit/doctest_text.txt which contains similar shared-state
# and exception cases.
