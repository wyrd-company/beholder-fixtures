"""Local, enclosing, global, and built-in resolution (PY-CAN-BIND-001)."""

from __future__ import annotations

MODULE_DEFAULT = "module-layer"


def read_four_levels(enclosing_value: str) -> dict[str, str]:
    """Read local, enclosing, global, and built-in bindings in one callable."""

    enclosing_marker = enclosing_value

    def inner() -> dict[str, str]:
        local_marker = "local-layer"
        return {
            "local": local_marker,
            "enclosing": enclosing_marker,
            "global": MODULE_DEFAULT,
            "builtin": str.__name__,
        }

    return inner()


def builtin_shadowing() -> str:
    """Shadow a built-in name and restore lexical access through qualification."""

    str = "shadowed-string"  # noqa: A001 — built-in shadowing variant
    shadowed = str
    del str
    return shadowed


def compile_time_local_classification(flag: bool) -> str:
    """Classify a name as local across branches before any assignment runs."""

    if flag:
        branch_marker = "taken"
    else:
        branch_marker = "skipped"

    def reader() -> str:
        return branch_marker

    return reader()


def compile_time_unbound_local_probe() -> tuple[tuple[str, ...], str]:
    """Expose compile-time local classification and the runtime unbound read."""

    def inner() -> str:
        if False:
            token = "never-assigned"
        return token

    try:
        inner()
        runtime = "no-error"
    except UnboundLocalError:
        runtime = "unbound-local"

    return inner.__code__.co_varnames, runtime


def class_scope_not_enclosing() -> str:
    """Show class body locals are not an enclosing function scope for methods."""

    outer_token = "outer-scope"

    class ScopeBoundary:
        class_token = "class-body"

        def method(self) -> str:
            return outer_token

    return ScopeBoundary().method()
