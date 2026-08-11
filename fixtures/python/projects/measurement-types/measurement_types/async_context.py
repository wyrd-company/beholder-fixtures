"""Async context managers (PY-CAN-PROT-007)."""

from __future__ import annotations

import asyncio
import contextlib
from types import TracebackType


class AsyncMeasurementScope:
    """Class-based async context manager."""

    def __init__(self, label: str) -> None:
        self.label = label
        self.entered = False
        self.exited = False

    async def __aenter__(self) -> str:
        await asyncio.sleep(0)
        self.entered = True
        return f"async:{self.label}"

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        await asyncio.sleep(0)
        self.exited = True
        return False


class AsyncSuppressingScope:
    """Async manager that suppresses ``ValueError``."""

    async def __aenter__(self) -> AsyncSuppressingScope:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        return exc_type is ValueError


@contextlib.asynccontextmanager
async def async_generator_measurement(label: str):
    """Generator-based async manager."""

    resource = f"async-gen:{label}"
    try:
        yield resource
    finally:
        await asyncio.sleep(0)


async def async_success_demo() -> str:
    """Exercise class-based async manager under success."""

    async with AsyncMeasurementScope("ok") as value:
        return value


async def async_exception_propagation_demo() -> str:
    """Propagate an exception from inside an async ``with``."""

    try:
        async with AsyncMeasurementScope("propagate"):
            raise ValueError("inner")
    except ValueError:
        return "propagated"
    return "no-error"


async def async_suppression_demo() -> str:
    """Suppress ``ValueError`` in an async manager."""

    async with AsyncSuppressingScope():
        raise ValueError("suppressed")
    return "suppressed"


async def async_multiple_nesting_demo() -> tuple[str, str]:
    """Use multiple async managers in one statement."""

    async with AsyncMeasurementScope("left") as a, async_generator_measurement("right") as b:
        return a, b


async def async_cancellation_cleanup_demo() -> str:
    """Show cleanup runs even when the body is cancelled."""

    cleanup_ran = False

    class TrackingScope:
        async def __aenter__(self) -> str:
            return "tracking"

        async def __aexit__(self, exc_type, exc, tb) -> bool:
            nonlocal cleanup_ran
            cleanup_ran = True
            return False

    async def cancellable_body() -> None:
        async with TrackingScope():
            await asyncio.sleep(0.05)

    task = asyncio.create_task(cancellable_body())
    await asyncio.sleep(0.01)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    return "cleanup" if cleanup_ran else "no-cleanup"


def sync_async_mismatch_demo() -> str:
    """Show that an async manager cannot be used with synchronous ``with``."""

    try:
        with AsyncMeasurementScope("mismatch") as _value:  # type: ignore[attr-defined]
            pass
        return "no-error"
    except AttributeError:
        return "attribute-error"
    except TypeError:
        return "type-error"
    except Exception as exc:
        return f"other:{type(exc).__name__}"
