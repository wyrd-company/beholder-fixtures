"""Exception chaining and traceback (PY-CAN-FLOW-003)."""

from __future__ import annotations

import traceback
import types


def implicit_context() -> dict[str, str]:
    """Implicit __context__ when raising inside handler without from."""
    try:
        try:
            raise ValueError("root-cause")
        except ValueError as root:
            raise RuntimeError("derived")
    except RuntimeError as derived:
        return {
            "context_type": type(derived.__context__).__name__ if derived.__context__ else "none",
            "cause": "none" if derived.__cause__ is None else type(derived.__cause__).__name__,
            "suppress": str(derived.__suppress_context__),
        }
    return {}


def explicit_cause() -> dict[str, str]:
    """Explicit cause via raise ... from ... sets __cause__ and suppresses __context__."""
    try:
        try:
            raise ValueError("root")
        except ValueError as root:
            raise RuntimeError("explicit") from root
    except RuntimeError as exc:
        return {
            "cause_type": type(exc.__cause__).__name__ if exc.__cause__ else "none",
            "suppress": str(exc.__suppress_context__),
            "context_type": type(exc.__context__).__name__ if exc.__context__ else "none",
        }
    return {}


def suppressed_context() -> dict[str, str]:
    """Suppressed context via raise ... from None clears chaining display."""
    try:
        try:
            raise ValueError("root")
        except ValueError:
            raise RuntimeError("suppressed") from None
    except RuntimeError as exc:
        return {
            "cause": "none" if exc.__cause__ is None else type(exc.__cause__).__name__,
            "suppress": str(exc.__suppress_context__),
            "context_type": type(exc.__context__).__name__ if exc.__context__ else "none",
        }
    return {}


def reraising_bare_preserves_traceback() -> dict[str, bool]:
    """Bare raise re-raises active exception preserving traceback object identity."""
    original_tb: types.TracebackType | None = None
    reraised_tb: types.TracebackType | None = None
    try:
        try:
            raise ValueError("trace-probe")
        except ValueError as e:
            original_tb = e.__traceback__
            raise
    except ValueError as e:
        reraised_tb = e.__traceback__
    return {
        "preserved": original_tb is not None and reraised_tb is not None,
        "same_object": original_tb is reraised_tb,
    }


def reraising_name_vs_bare() -> dict[str, str]:
    """Raise e (by name) versus bare raise — traceback handling differs."""
    # Bare raise preserves original traceback chain; raise e re-raises same
    # instance but creates a new traceback frame at raise site when handler
    # mutates or rebinds.
    def via_bare() -> str:
        try:
            try:
                raise ValueError("via-bare")
            except ValueError:
                raise
        except ValueError as exc:
            return f"bare-{exc.__traceback__.tb_lineno if exc.__traceback__ else 0}"

    def via_name() -> str:
        try:
            try:
                raise ValueError("via-name")
            except ValueError as exc:
                caught = exc
                raise caught
        except ValueError as exc:
            return f"name-{exc.__traceback__.tb_lineno if exc.__traceback__ else 0}"

    return {"bare": via_bare(), "name": via_name()}


def traceback_mutation() -> str:
    """Traceback grows as exception propagates through handlers."""
    try:
        try:
            raise ValueError("level-1")
        except ValueError as e:
            raise RuntimeError("level-2") from e
    except RuntimeError as exc:
        tb_lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
        return "".join(tb_lines)[:200]
    return ""


def exception_in_handler() -> str:
    """New exception raised inside handler replaces handling flow."""
    try:
        try:
            raise ValueError("initial")
        except ValueError:
            raise TypeError("handler-failure")
    except TypeError:
        return "handler-failure-caught"
    except ValueError:
        return "initial-still"
    return "unreachable"


def exception_in_finally() -> str:
    """Exception in finally suppresses prior exception (or chains it)."""
    try:
        try:
            raise ValueError("try-failure")
        finally:
            raise RuntimeError("finally-failure")
    except RuntimeError as exc:
        # Original ValueError becomes __context__
        return f"finally-wins-context-{type(exc.__context__).__name__ if exc.__context__ else 'none'}"
    except ValueError:
        return "try-wins"
    return "unreachable"


def structured_fields_over_text() -> dict[str, str]:
    """Use structured fields rather than message text for programmatic checks."""
    try:
        try:
            raise ValueError("structured-root")
        except ValueError as root:
            err = RuntimeError("structured-derived")
            err.__cause__ = root
            raise err
    except RuntimeError as exc:
        tb = exc.__traceback__
        return {
            "cause_type": type(exc.__cause__).__name__ if exc.__cause__ else "none",
            "traceback_present": str(tb is not None),
            "notes_present": str(bool(getattr(exc, "__notes__", []))),
        }
    return {}


def traceback_preservation_with_notes() -> dict[str, object]:
    """Preserve traceback and attach notes as structured metadata (3.11+)."""
    try:
        raise ValueError("with-notes")
    except ValueError as exc:
        exc.add_note("job-id: 42")
        exc.add_note("retryable: true")
        tb_before = exc.__traceback__
        try:
            raise
        except ValueError as reraised:
            return {
                "notes": list(getattr(reraised, "__notes__", [])),
                "traceback_preserved": reraised.__traceback__ is tb_before,
            }
    return {}
