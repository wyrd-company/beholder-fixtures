"""Callable types and parameter specifications (PY-CAN-TYPE-008)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Concatenate, ParamSpec, Protocol, TypeVar

T = TypeVar("T")
P = ParamSpec("P")
Q = ParamSpec("Q")

# --- Higher-order function with Callable -------------------------------------

def apply_twice(func: Callable[[int], int], value: int) -> int:
    return func(func(value))


def increment(n: int) -> int:
    return n + 1


# --- Callback protocol (alternative to Callable) ------------------------------

class Combiner(Protocol):
    def __call__(self, a: int, b: int) -> int: ...


def combine(a: int, b: int) -> int:
    return a + b


def use_combiner(func: Combiner, x: int, y: int) -> int:
    return func(x, y)


# --- Ellipsis unknown signature variant ---------------------------------------

def unknown_signature(func: Callable[..., int]) -> int:
    return func(1, "extra", key="value")


def any_callable_demo(func: Callable[..., object]) -> object:
    return func()


# --- Keyword names and kinds variant -----------------------------------------

def keyword_aware(func: Callable[Concatenate[str, P], int]) -> Callable[P, int]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> int:
        return func("prefix", *args, **kwargs)
    return wrapper


# --- Runtime callable does not check signature -------------------------------

def runtime_callable_no_check_demo() -> str:
    def typed_target(x: int, y: str) -> str:
        return f"{x}:{y}"

    # At runtime any callable satisfying ``callable()`` passes; signature not enforced
    untyped: Callable[..., str] = typed_target  # type: ignore[assignment]
    return untyped(1, "hello")  # type: ignore[arg-type]


# --- ParamSpec signature-preserving decorator ---------------------------------

def preserving_decorator(func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return func(*args, **kwargs)
    return wrapper


@preserving_decorator
def greet(name: str, *, loud: bool = False) -> str:
    msg = f"hello {name}"
    return msg.upper() if loud else msg


# --- ParamSpec signature-transforming decorator --------------------------------

def adding_prefix(func: Callable[P, T]) -> Callable[Concatenate[str, P], T]:
    def wrapper(prefix: str, *args: P.args, **kwargs: P.kwargs) -> T:
        _ = prefix
        return func(*args, **kwargs)
    return wrapper


def base_handler(value: int) -> str:
    return str(value)


prefixed_handler = adding_prefix(base_handler)


# --- Valid use of ParamSpec.args / ParamSpec.kwargs --------------------------

def forward_args(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    return func(*args, **kwargs)


def uses_args_kwargs_demo() -> str:
    return forward_args(greet, "world", loud=True)


# --- Concatenate variant ------------------------------------------------------

def with_concatenate(func: Callable[Concatenate[int, P], T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return func(42, *args, **kwargs)
    return wrapper
