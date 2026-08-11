"""Decorator evaluation and application (PY-CAN-CALL-005)."""

from __future__ import annotations

import functools
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

evaluation_log: list[str] = []
registry: list[Callable[..., Any]] = []


def parameterized(tag: str) -> Callable[[F], F]:
    """Parameterized decorator factory that records evaluation time."""

    evaluation_log.append(f"param:{tag}")

    def decorator(func: F) -> F:
        evaluation_log.append(f"apply:{tag}:{func.__name__}")

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


def registering(func: F) -> F:
    """Registering decorator that records application and preserves the function."""

    evaluation_log.append(f"register:{func.__name__}")
    registry.append(func)
    return func


def metadata_preserving(func: F) -> F:
    """Decorator that preserves metadata and exposes ``__wrapped__``."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrapper preserving signature."""

        return func(*args, **kwargs)

    return wrapper  # type: ignore[return-value]


def replacing(func: Callable[..., Any]) -> int:
    """Replacing decorator that yields a non-callable result."""

    return 42


# Stacked decorators — application is bottom-up.
@parameterized("outer")
@registering
@metadata_preserving
def stacked_handler(value: str) -> str:
    """Handler with stacked decorators."""

    return f"stacked:{value}"


# Arbitrary expression decorator (PEP 614): any expression since 3.9.
def tag_decorator(label: str) -> Callable[[F], F]:
    def deco(func: F) -> F:
        func._decorator_tag = label  # type: ignore[attr-defined]
        return func

    return deco


@(tag_decorator("parcel") if True else tag_decorator("fallback"))
def arbitrary_expression_target(value: str) -> str:
    """Target decorated via an arbitrary conditional expression."""

    return f"arbitrary:{value}"


# Non-callable replacement
@replacing
def replaced_target() -> str:
    """This binding becomes an int after decoration."""

    return "should-not-run"


# Ordering with descriptors: classmethod + custom decorator, both orders.

evaluation_descriptor_log: list[str] = []


def describe_order(label: str) -> Callable[[Any], Any]:
    evaluation_descriptor_log.append(f"eval:{label}")

    def decorator(obj: Any) -> Any:
        evaluation_descriptor_log.append(f"apply:{label}:{getattr(obj, '__name__', str(obj))}")
        return obj

    return decorator


class DescriptorOrdering:
    """Exercise ordering between descriptors and plain decorators."""

    @describe_order("descriptor-first")
    @classmethod
    def via_classmethod(cls, label: str) -> str:
        return f"cm:{cls.__name__}:{label}"

    @classmethod
    @describe_order("descriptor-second")
    def via_wrapped_classmethod(cls, label: str) -> str:
        return f"cm2:{cls.__name__}:{label}"

    @describe_order("function-then-static")
    @staticmethod
    def via_static(label: str) -> str:
        return f"static:{label}"


def stacked_application_order() -> list[str]:
    """Return the log proving decorator evaluation (top-down) vs application (bottom-up)."""

    return list(evaluation_log)


def replacing_is_non_callable() -> bool:
    """Check that the replacing decorator left a non-callable."""

    return isinstance(replaced_target, int)


def wrapped_access() -> Callable[..., Any]:
    """Expose ``__wrapped__`` chain from the stacking example."""

    return stacked_handler.__wrapped__  # type: ignore[attr-defined]


def arbitrary_expression_metadata() -> str:
    """Read the tag placed by the arbitrary-expression decorator."""

    return arbitrary_expression_target._decorator_tag  # type: ignore[attr-defined]
