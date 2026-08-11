"""Exception groups and except* (PY-CAN-FLOW-005)."""

from __future__ import annotations


def split_and_handle() -> dict[str, list[str]]:
    """Split group by type via except*."""
    results: dict[str, list[str]] = {"retryable": [], "fatal": []}
    try:
        raise BaseExceptionGroup(
            "job-batch",
            [
                ValueError("bad-value"),
                RuntimeError("runtime-failure"),
                ValueError("another-bad"),
            ],
        )
    except* ValueError as eg:
        results["retryable"] = [e.args[0] for e in eg.exceptions]
    except* RuntimeError as eg:
        results["fatal"] = [e.args[0] for e in eg.exceptions]
    return results


def partially_handle_and_reraise() -> str:
    """Partially handle group: handled part is removed, remainder propagates."""
    outcome = "no-exception"
    try:
        try:
            raise BaseExceptionGroup(
                "partial",
                [ValueError("handled"), RuntimeError("unhandled")],
            )
        except* ValueError:
            pass
    except* RuntimeError as eg:
        outcome = f"remaining-{len(eg.exceptions)}"
    except* BaseException:
        outcome = "unexpected-group"
    return outcome


def nest_groups() -> str:
    """Nested ExceptionGroups preserve structure through handling."""
    inner = BaseExceptionGroup("inner", [ValueError("v1"), TypeError("t1")])
    outer = BaseExceptionGroup("outer", [inner, RuntimeError("r1")])
    outcome = "done"
    try:
        raise outer
    except* ValueError as eg:
        outcome = f"nested-value-{len(eg.exceptions)}"
    except* (TypeError, RuntimeError):
        pass
    return outcome


def merge_failures() -> str:
    """Merge multiple failures into one group programmatically."""
    errors: list[BaseException] = []
    for msg, typ in [("a", ValueError), ("b", RuntimeError), ("c", ValueError)]:
        errors.append(typ(msg))
    group = BaseExceptionGroup("merged", errors)
    return f"merged-{len(group.exceptions)}"


def derived_group() -> str:
    """Derived ExceptionGroup subclass is caught by base except* as well."""
    class JobExceptionGroup(BaseExceptionGroup):
        pass

    outcome = "unhandled"
    try:
        raise JobExceptionGroup("derived", [ValueError("v"), ValueError("v2")])
    except* ValueError as eg:
        outcome = f"derived-caught-{len(eg.exceptions)}"
    return outcome


def single_exception_wrapping_note() -> str:
    """Single sub-exception still forms a group of one when wrapped."""
    single = BaseExceptionGroup("single", [ValueError("only-one")])
    return f"single-len-{len(single.exceptions)}-is-group-{isinstance(single, BaseExceptionGroup)}"


def forbidden_control_flow_note() -> str:
    """except* cannot be mixed with except in same try; break/continue inside except* is forbidden."""
    return "mixing-ordinary-and-star-is-syntax-error; break-inside-except-star-is-syntax-error"


def reraising_group() -> str:
    """Reraising inside except* propagates remaining or new group."""
    outcome = "no-group"
    try:
        try:
            raise BaseExceptionGroup("reraised", [ValueError("v"), ValueError("v2")])
        except* ValueError as eg:
            raise BaseExceptionGroup("from-handler", list(eg.exceptions)) from None
    except BaseExceptionGroup as eg:
        outcome = f"reraised-{len(eg.exceptions)}"
    return outcome


def cannot_mix_handlers_demonstration() -> str:
    """Valid code keeps star handlers separate from ordinary handlers across tries."""
    try:
        raise ValueError("ordinary")
    except ValueError:
        ordinary = "ordinary-caught"

    try:
        raise BaseExceptionGroup("star", [ValueError("star-val")])
    except* ValueError:
        star = "star-caught"

    return f"{ordinary}-{star}"
