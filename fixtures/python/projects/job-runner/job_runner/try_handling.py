"""try/except/else/finally precedence (PY-CAN-FLOW-002)."""

from __future__ import annotations


def normal_flow() -> str:
    """No exception — else runs, finally always runs."""
    log: list[str] = []
    try:
        log.append("try")
    except ValueError:
        log.append("except")
    else:
        log.append("else")
    finally:
        log.append("finally")
    return "-".join(log)


def matched_handler(value: int) -> str:
    """Matched except runs, else is skipped."""
    try:
        if value < 0:
            raise ValueError("negative")
    except ValueError:
        return "matched"
    else:
        return "else"
    finally:
        pass
    return "unreachable"


def unmatched_handler(value: int) -> str:
    """Matched ValueError is caught; TypeError propagates as truly unmatched."""
    try:
        if value == 1:
            raise ValueError("value-bad")
        if value == 2:
            raise TypeError("type-bad")
    except ValueError:
        return "matched-value"
    else:
        return "else-no-exception"
    # TypeError is not caught here and propagates to caller as unmatched variant
    return "done"


def bare_handler(value: int) -> str:
    """Bare except catches any exception."""
    try:
        if value == 0:
            raise RuntimeError("any")
    except:  # noqa: E722 — bare handler variant
        return "bare-caught"
    else:
        return "no-exception"
    finally:
        pass
    return "after"


def tuple_handler(value: int) -> str:
    """Tuple handler catches any member type."""
    try:
        if value == 1:
            raise ValueError("v")
        if value == 2:
            raise TypeError("t")
    except (ValueError, TypeError) as exc:
        return f"tuple-caught-{type(exc).__name__}"
    else:
        return "else"
    return "after"


def handler_raised_replacement() -> str:
    """Exception raised inside handler replaces original via chaining."""
    try:
        try:
            raise ValueError("initial")
        except ValueError as original:
            raise RuntimeError("replacement") from original
    except RuntimeError as exc:
        return f"replaced-cause-{type(exc.__cause__).__name__}"
    return "unreachable"


def return_and_finally_override() -> str:
    """Finally return overrides try return; else skipped when return occurs."""
    def _with_override() -> str:
        try:
            return "try-return"
        finally:
            return "finally-override"

    def _else_skipped_on_return() -> str:
        try:
            return "early-return"
        except ValueError:
            return "except"
        else:
            return "else-should-not-run"
        finally:
            pass

    return f"{_with_override()}-{_else_skipped_on_return()}"


def saved_vs_active_exception() -> dict[str, str]:
    """Saved reference survives; active handler name is cleared after block."""
    saved: ValueError | None = None
    active_cleared = "unknown"
    try:
        raise ValueError("job-error")
    except ValueError as exc:
        saved = exc
        active_inside = exc.args[0]
        _ = active_inside
    # After handler, the name `exc` is deleted (Python clears it).
    try:
        _ = exc  # type: ignore[name-defined]  # noqa: F821
        active_cleared = "still-bound"
    except NameError:
        active_cleared = "cleared"
    return {"saved": saved.args[0] if saved else "none", "active": active_cleared}


def chained_replacement_explicit() -> str:
    """Chained replacement via explicit cause vs implicit context."""
    try:
        try:
            raise ValueError("root")
        except ValueError as e:
            raise KeyError("derived") from e
    except KeyError as ke:
        cause = type(ke.__cause__).__name__ if ke.__cause__ else "none"
        context = type(ke.__context__).__name__ if ke.__context__ else "none"
        return f"cause-{cause}-context-{context}"
    return "unreachable"


def try_else_finally_precedence() -> str:
    """Cover else only when no exception and finally always executes."""
    order: list[str] = []

    # Normal path: try -> else -> finally
    try:
        order.append("try-normal")
    except ValueError:
        order.append("except")
    else:
        order.append("else-normal")
    finally:
        order.append("finally-normal")

    # Exception path: try -> except -> finally (else skipped)
    try:
        raise ValueError("probe")
    except ValueError:
        order.append("except-matched")
    else:
        order.append("else-skipped")
    finally:
        order.append("finally-after-except")

    # Propagating finally: finally runs even when handler re-raises
    try:
        try:
            raise ValueError("inner")
        except ValueError:
            order.append("inner-except")
            raise
        else:
            order.append("inner-else")
        finally:
            order.append("inner-finally")
    except ValueError:
        order.append("outer-caught")

    return "-".join(order)
