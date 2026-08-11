"""Context managers (PY-CAN-PROT-006)."""

from __future__ import annotations

import contextlib
from types import TracebackType


class MeasurementScope:
    """Class-based context manager where enter result differs from manager."""

    def __init__(self, label: str) -> None:
        self.label = label
        self.entered = False
        self.exited: tuple[type[BaseException] | None, BaseException | None, TracebackType | None] | None = None

    def __enter__(self) -> str:
        self.entered = True
        return f"scope:{self.label}"

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        self.exited = (exc_type, exc, tb)
        return False


class SuppressingScope:
    """Context manager that suppresses a specific exception."""

    def __enter__(self) -> SuppressingScope:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        if exc_type is ValueError:
            return True
        return False


class RaisingExitScope:
    """``__exit__`` raises, replacing the original exception."""

    def __enter__(self) -> RaisingExitScope:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        raise RuntimeError("exit-replacement")


class PartialSetupScope:
    """``__enter__`` acquires then fails, requiring staged cleanup."""

    def __init__(self) -> None:
        self.acquired = False

    def __enter__(self) -> str:
        self.acquired = True
        raise RuntimeError("setup-failure")

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        return False

    def release(self) -> None:
        """Release the staged acquisition."""
        self.acquired = False


@contextlib.contextmanager
def generator_measurement(label: str):
    """Generator-based manager yielding a distinct enter value."""

    resource = f"gen:{label}"
    try:
        yield resource
    finally:
        pass


def multiple_managers_demo() -> tuple[str, str]:
    """Use multiple managers in one ``with`` statement."""

    left = MeasurementScope("left")
    right = MeasurementScope("right")
    with left as a, right as b:
        return a, b


def nested_equivalence_demo() -> tuple[str, str]:
    """Show ``with a, b`` equivalence to nested ``with``."""

    first = MeasurementScope("first")
    second = MeasurementScope("second")
    with first as a:
        with second as b:
            return a, b


def suppression_demo() -> str:
    """Suppress ``ValueError`` while propagating other exceptions."""

    with SuppressingScope():
        raise ValueError("suppressed")
    try:
        with SuppressingScope():
            raise TypeError("propagated")
        return "no-error"
    except TypeError:
        return "propagated"


def exit_raises_replaces_demo() -> str:
    """``__exit__`` raise replaces an active exception."""

    try:
        with RaisingExitScope():
            raise ValueError("original")
    except RuntimeError as exc:
        return str(exc)
    except ValueError:
        return "original-preserved"
    return "no-error"


def partial_setup_cleanup_demo() -> str:
    """Handle a failing ``__enter__`` with explicit staged cleanup."""

    scope = PartialSetupScope()
    try:
        with scope:
            return "no-error"
    except RuntimeError as exc:
        # ``__exit__`` is not called when ``__enter__`` raises, so the
        # caller must release the acquisition explicitly.
        if scope.acquired:
            scope.release()
        return f"{exc}:released:{not scope.acquired}"


def exitstack_demo() -> list[str]:
    """Compose managers with ``ExitStack``."""

    log: list[str] = []
    with contextlib.ExitStack() as stack:
        a = stack.enter_context(MeasurementScope("a"))
        b = stack.enter_context(generator_measurement("b"))
        log.extend([a, b])
    return log


def enter_result_differs_demo() -> bool:
    """Verify that ``__enter__`` result differs from the manager identity."""

    manager = MeasurementScope("check")
    with manager as value:
        return value is not manager
