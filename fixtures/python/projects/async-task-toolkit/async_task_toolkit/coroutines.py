"""Native coroutines and awaitables (PY-CAN-CALL-012)."""

from __future__ import annotations

import asyncio
import inspect
import warnings


async def parcel_fetch(label: str) -> str:
    """Native coroutine whose body does not run until awaited."""

    await asyncio.sleep(0)
    return f"fetched:{label}"


class CustomAwaitable:
    """Custom awaitable implementing ``__await__``."""

    def __init__(self, value: str) -> None:
        self.value = value

    def __await__(self):  # type: ignore[no-untyped-def]
        yield
        return f"awaited:{self.value}"


def calling_does_not_run_body() -> dict[str, object]:
    """Calling a coroutine function returns a coroutine object without running the body."""

    coro = parcel_fetch("parcel-a")
    is_coro = inspect.iscoroutine(coro)
    # Body hasn't run; coroutine not yet awaited.
    coro.close()
    return {"is_coroutine": is_coro, "type_name": type(coro).__name__}


async def schedule_and_await() -> dict[str, str]:
    """Create, schedule, and await coroutines and custom awaitables."""

    result = await parcel_fetch("parcel-b")
    custom = await CustomAwaitable("parcel-c")
    task = asyncio.create_task(parcel_fetch("parcel-d"))
    tasked = await task
    return {"coroutine": result, "custom": custom, "tasked": tasked}


def await_twice_failure() -> str:
    """Awaiting the same coroutine object twice must raise ``RuntimeError``."""

    async def run() -> str:
        coro = parcel_fetch("twice")
        first = await coro
        try:
            await coro
            return "no-error"
        except RuntimeError:
            return "runtime-error"

    return asyncio.run(run())


def unawaited_diagnostic() -> str:
    """Un-awaited coroutines emit ``RuntimeWarning`` when collected."""

    async def inner() -> str:
        return "never-awaited"

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", RuntimeWarning)
        coro = inner()
        del coro
        import gc

        gc.collect()
        has_warning = any(issubclass(w.category, RuntimeWarning) for w in caught)
    # Fallback: explicitly check coroutine was not awaited via close warning.
    return "runtime-warning" if has_warning else "no-warning-or-closed"


async def cancellation_at_suspension() -> str:
    """Cancellation propagates at the suspension point."""

    async def cancellable() -> str:
        try:
            await asyncio.sleep(0.1)
            return "completed"
        except asyncio.CancelledError:
            return "cancelled"

    task = asyncio.create_task(cancellable())
    await asyncio.sleep(0)
    task.cancel()
    return await task


def cancellation_demo() -> str:
    """Run the cancellation exercise in a fresh event loop."""

    return asyncio.run(cancellation_at_suspension())


def coroutine_inspection() -> dict[str, object]:
    """Inspect coroutine object properties."""

    coro = parcel_fetch("inspect")
    info = {
        "is_coroutine_function": inspect.iscoroutinefunction(parcel_fetch),
        "is_coroutine": inspect.iscoroutine(coro),
        "is_awaitable": inspect.isawaitable(coro),
    }
    coro.close()
    return info
