"""Custom exception hierarchies (PY-CAN-FLOW-004)."""

from __future__ import annotations

import pickle


class JobError(Exception):
    """Base for job runner failures."""

    def __init__(self, message: str, *, job_id: str = "unknown") -> None:
        super().__init__(message)
        self.job_id = job_id


class JobRetryableError(JobError):
    """Transient failure that may be retried."""


class JobFatalError(JobError):
    """Permanent failure that should not be retried."""

    def __init__(self, message: str, *, job_id: str = "unknown", code: int = 0) -> None:
        super().__init__(message, job_id=job_id)
        self.code = code


class JobTimeoutError(JobRetryableError):
    """Retryable timeout with deadline context."""

    def __init__(self, message: str, *, job_id: str = "unknown", deadline_ms: int = 0) -> None:
        super().__init__(message, job_id=job_id)
        self.deadline_ms = deadline_ms


class JobValidationError(JobFatalError):
    """Fatal validation failure with field detail."""

    def __init__(
        self,
        message: str,
        *,
        job_id: str = "unknown",
        code: int = 0,
        field: str = "",
    ) -> None:
        super().__init__(message, job_id=job_id, code=code)
        self.field = field


def handling_by_base_and_leaf() -> dict[str, str]:
    """Base handler catches leaf; leaf handler does not catch sibling branch."""
    results: dict[str, str] = {}

    # Catch by base
    try:
        raise JobTimeoutError("timed out", job_id="job-1", deadline_ms=100)
    except JobError as exc:
        results["base_caught"] = type(exc).__name__

    # Catch by leaf only
    try:
        raise JobRetryableError("retry", job_id="job-2")
    except JobTimeoutError:
        results["leaf_caught_sibling"] = "unexpected"
    except JobRetryableError:
        results["leaf_caught_exact"] = "retryable"

    # Base does not catch unrelated branch
    try:
        raise JobValidationError("bad field", job_id="job-3", field="payload")
    except JobRetryableError:
        results["retryable_caught_fatal"] = "unexpected"
    except JobFatalError as exc:
        results["fatal_caught"] = type(exc).__name__

    return results


def args_and_attributes_preserved() -> dict[str, object]:
    """Args tuple and custom attributes round-trip through raise/catch."""
    try:
        raise JobValidationError("invalid", job_id="job-7", code=422, field="count")
    except JobValidationError as exc:
        return {
            "args": exc.args,
            "job_id": exc.job_id,
            "code": exc.code,
            "field": exc.field,
        }
    return {}


def notes_support() -> list[str]:
    """add_note is available on BaseException since Python 3.11."""
    err = JobTimeoutError("deadline", job_id="job-9", deadline_ms=50)
    err.add_note("attempt: 2/3")
    err.add_note("hint: increase deadline_ms")
    return list(getattr(err, "__notes__", []))


def serialization_round_trip() -> dict[str, object]:
    """Exception survives pickle round-trip preserving args and attributes."""
    original = JobFatalError("fatal", job_id="job-11", code=500)
    original.add_note("note-for-serialization")
    data = pickle.dumps(original)
    restored: JobFatalError = pickle.loads(data)
    return {
        "type": type(restored).__name__,
        "args": restored.args,
        "job_id": restored.job_id,
        "code": restored.code,
        "notes": list(getattr(restored, "__notes__", [])),
    }


def bad_constructor_compatibility() -> dict[str, str]:
    """Calling hierarchy with wrong arguments raises TypeError, not JobError."""
    outcomes: dict[str, str] = {}
    try:
        # JobTimeoutError requires deadline_ms keyword; missing is handled via default
        # but extra positional arg is rejected.
        JobTimeoutError("msg", "extra-pos-arg")  # type: ignore[arg-type]
    except TypeError as exc:
        outcomes["extra_pos"] = type(exc).__name__
    try:
        JobValidationError()  # type: ignore[call-arg] — missing required message
    except TypeError as exc:
        outcomes["missing_arg"] = type(exc).__name__
    return outcomes


def single_inheritance_hierarchy_note() -> str:
    """Hierarchy uses single inheritance only; multiple inheritance discouraged."""
    # All Job* errors inherit linearly from JobError; no diamond.
    bases = [c.__name__ for c in JobTimeoutError.__mro__]
    return "->".join(bases)
