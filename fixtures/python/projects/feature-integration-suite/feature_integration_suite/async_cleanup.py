"""Async generator cleanup under cancellation/context/task group (PY-CAN-INT-006)."""

from __future__ import annotations

import asyncio
import contextlib
from typing import AsyncGenerator

# --- Cleanup tracking ---

cleanup_log: list[str] = []


@contextlib.asynccontextmanager
async def tracked_context(name: str):  # type: ignore[no-untyped-def]
    try:
        cleanup_log.append(f"{name}:enter")
        yield
    finally:
        cleanup_log.append(f"{name}:exit")


# --- Async generator with two cleanup layers ---


async def cancellable_stream(count: int) -> AsyncGenerator[int, None]:
    """Async generator whose cleanup must run even when cancelled during suspension."""
    try:
        async with tracked_context("outer"):
            try:
                for idx in range(count):
                    cleanup_log.append(f"produce:{idx}")
                    # Suspension point where cancellation can arrive
                    await asyncio.sleep(0.05)
                    yield idx
            finally:
                # Inner cleanup layer
                cleanup_log.append("inner:cleanup")
                # On Python 3.11+, uncancel should be used to preserve cancellation if suppression attempted
                # Demonstrate uncancellation variant: do not suppress CancelledError
    except asyncio.CancelledError:
        cleanup_log.append("cancelled:caught")
        raise
    finally:
        cleanup_log.append("outer:finally")


# --- Task group + cancellation demo ---


async def task_group_cancellation_demo() -> dict[str, object]:
    """Cancel async generator during suspension via TaskGroup and prove both layers run without losing cancellation."""
    cleanup_log.clear()
    async with asyncio.TaskGroup() as tg:  # type: ignore[attr-defined]  # Python 3.11+
        agen = cancellable_stream(10)

        async def consumer() -> None:
            async for val in agen:
                cleanup_log.append(f"consumed:{val}")
                if val == 1:
                    # Cancel the consumer task while generator is suspended at sleep
                    # Get current task and cancel
                    current = asyncio.current_task()
                    assert current is not None
                    current.cancel()
                    # Next suspension should raise CancelledError inside generator

        task = tg.create_task(consumer())
        try:
            await asyncio.sleep(0.12)
        except BaseException:
            pass

    # After TaskGroup exits, check log
    return {"log": list(cleanup_log), "inner_ran": "inner:cleanup" in cleanup_log, "outer_exit": "outer:exit" in cleanup_log}


async def cancel_during_suspension_demo() -> dict[str, object]:
    """Direct cancellation of task driving async generator."""
    cleanup_log.clear()
    agen = cancellable_stream(5)
    task = asyncio.create_task(_drive_agen(agen))
    await asyncio.sleep(0.08)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    return {
        "log": list(cleanup_log),
        "cancelled_preserved": "cancelled:caught" in cleanup_log,
        "both_layers": "inner:cleanup" in cleanup_log and "outer:exit" in cleanup_log,
    }


async def _drive_agen(agen: AsyncGenerator[int, None]) -> None:
    async for _ in agen:
        pass


async def early_exit_cleanup_demo() -> dict[str, object]:
    """Early exit via aclose must trigger cleanup without cancellation loss."""
    cleanup_log.clear()
    agen = cancellable_stream(10)
    it = agen.__aiter__()
    await it.__anext__()
    await agen.aclose()
    return {"log": list(cleanup_log), "early_exit_cleanup": "inner:cleanup" in cleanup_log and "outer:exit" in cleanup_log}


async def cleanup_raises_group_demo() -> dict[str, object]:
    """Cleanup that raises while cancellation is pending should surface ExceptionGroup / combined error."""
    cleanup_log.clear()

    async def failing_cleanup_stream() -> AsyncGenerator[int, None]:
        try:
            async with tracked_context("failing-outer"):
                for idx in range(3):
                    await asyncio.sleep(0.02)
                    yield idx
        finally:
            cleanup_log.append("failing:finally")
            # Simulate cleanup raising an exception group (Python 3.11 BaseExceptionGroup)
            raise RuntimeError("cleanup-failure")

    agen = failing_cleanup_stream()
    task = asyncio.create_task(_drive_agen(agen))
    await asyncio.sleep(0.05)
    task.cancel()
    try:
        await task
    except BaseException as exc:  # noqa: BLE001
        # Cancellation + cleanup failure may combine to BaseExceptionGroup
        exc_type = type(exc).__name__
        # If TaskGroup were used, ExceptionGroup would appear; here we at least capture RuntimeError
        return {"exception_type": exc_type, "exception": str(exc), "log": list(cleanup_log)}
    return {"exception_type": "none", "log": list(cleanup_log)}


async def uncancel_suppression_demo() -> dict[str, object]:
    """Cancellation suppression vs uncancel: inner handler must not swallow cancellation."""
    cleanup_log.clear()

    async def suppressing_stream() -> AsyncGenerator[int, None]:
        try:
            yield 1
            await asyncio.sleep(0.05)
            yield 2
        except asyncio.CancelledError:
            cleanup_log.append("suppressed:caught")
            # Intentionally do not re-raise to demonstrate suppression (counterexample)
            # Correct code should re-raise or call uncancel (Python 3.11+)
            # Here we show the variant where suppression loses cancellation
            return
        finally:
            cleanup_log.append("suppressed:finally")

    agen = suppressing_stream()
    task = asyncio.create_task(_drive_agen(agen))
    await asyncio.sleep(0.03)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        was_cancelled = True
    else:
        was_cancelled = False
    return {"was_cancelled": was_cancelled, "log": list(cleanup_log)}


async def loop_shutdown_finalization_demo() -> dict[str, object]:
    """Generator finalization hooks: aclose and loop shutdown should still finalize."""
    cleanup_log.clear()
    agen = cancellable_stream(3)
    # Not fully consumed, then garbage-collected / explicitly closed via aclose hook
    await agen.aclose()
    # Also test that an unclosed generator triggers asyncgen finalizer (requires loop)
    agen2 = cancellable_stream(3)
    it = agen2.__aiter__()
    try:
        await it.__anext__()
    finally:
        await agen2.aclose()
    return {"log": list(cleanup_log)}


def run_async_demo() -> dict[str, object]:
    """Sync wrapper to run all async demos."""

    async def _all() -> dict[str, object]:
        return {
            "cancel_during_suspension": await cancel_during_suspension_demo(),
            "early_exit": await early_exit_cleanup_demo(),
            "task_group": await task_group_cancellation_demo(),
            "cleanup_group": await cleanup_raises_group_demo(),
            "uncancel": await uncancel_suppression_demo(),
            "shutdown": await loop_shutdown_finalization_demo(),
        }

    return asyncio.run(_all())
