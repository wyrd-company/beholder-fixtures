"""Async generator cleanup under cancellation/context/task group (PY-CAN-INT-006)."""

from __future__ import annotations

import asyncio
import contextlib
from typing import AsyncGenerator

# --- Cleanup tracking ---

cleanup_log: list[str] = []


class _TrackedContext:
    def __init__(self, name: str) -> None:
        self.name = name

    async def __aenter__(self) -> None:
        cleanup_log.append(f"{self.name}:enter")
        return None

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> bool:
        cleanup_log.append(f"{self.name}:exit")
        return False


def tracked_context(name: str) -> _TrackedContext:  # type: ignore[no-untyped-def]
    return _TrackedContext(name)


# --- Async generator with two cleanup layers ---


async def cancellable_stream(count: int) -> AsyncGenerator[int, None]:
    """Async generator whose cleanup must run even when cancelled during suspension or loop shutdown."""
    try:
        async with tracked_context("outer"):
            try:
                for idx in range(count):
                    cleanup_log.append(f"produce:{idx}")
                    # Suspension point where cancellation or GeneratorExit can arrive
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
    except GeneratorExit:
        cleanup_log.append("generator-exit:caught")
        return
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
    """Cleanup that raises group while cancellation is pending should surface ExceptionGroup."""
    cleanup_log.clear()

    async def failing_cleanup_stream() -> AsyncGenerator[int, None]:
        try:
            async with tracked_context("failing-outer"):
                for idx in range(3):
                    await asyncio.sleep(0.02)
                    yield idx
        finally:
            cleanup_log.append("failing:finally")
            # Grouped cleanup failure: two distinct errors as ExceptionGroup
            raise BaseExceptionGroup("cleanup-group", [RuntimeError("cleanup-a"), ValueError("cleanup-b")])

    # Use TaskGroup so cancellation and grouped cleanup combine to visible ExceptionGroup
    try:
        async with asyncio.TaskGroup() as tg:  # type: ignore[attr-defined]
            agen = failing_cleanup_stream()

            async def driver() -> None:
                async for _ in agen:
                    pass

            task = tg.create_task(driver())
            await asyncio.sleep(0.05)
            task.cancel()
            # TaskGroup will collect cancellation + cleanup group
    except BaseException as exc:  # noqa: BLE001
        exc_type = type(exc).__name__
        # ExceptionGroup should surface with two sub-exceptions
        sub_types: list[str] = []
        if isinstance(exc, BaseExceptionGroup):
            for sub in exc.exceptions:  # type: ignore[attr-defined]
                sub_types.append(type(sub).__name__)
                # Flatten nested CancelledError + group
                if isinstance(sub, BaseExceptionGroup):
                    for inner in sub.exceptions:  # type: ignore[attr-defined]
                        sub_types.append(type(inner).__name__)
        return {
            "exception_type": exc_type,
            "exception": str(exc),
            "sub_types": sub_types,
            "is_group": isinstance(exc, BaseExceptionGroup),
            "log": list(cleanup_log),
        }
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


def _loop_shutdown_sync() -> dict[str, object]:
    """Sync helper that uses a fresh loop to demonstrate shutdown-asyncgens finalization."""
    cleanup_log.clear()
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)

        async def start_without_close():
            agen = cancellable_stream(3)
            await agen.__anext__()  # start and suspend inside tracked_context
            # Do NOT call aclose; return agen so loop keeps it alive for shutdown phase
            return agen

        agen = loop.run_until_complete(start_without_close())
        # agen is still open, suspended at await sleep inside outer context; shutdown_asyncgens will finalize
        loop.run_until_complete(loop.shutdown_asyncgens())
        # Keep reference to prove we did not call explicit aclose on this instance
        _ = agen
        return {
            "log": list(cleanup_log),
            "shutdown_triggered": "inner:cleanup" in cleanup_log and "outer:exit" in cleanup_log,
            "used_shutdown_asyncgens": True,
            "explicit_aclose_not_called": True,
        }
    finally:
        asyncio.set_event_loop(None)
        loop.close()


async def loop_shutdown_finalization_demo() -> dict[str, object]:
    """Generator finalization via loop shutdown-asyncgens, distinct from explicit aclose."""
    # Run sync helper in thread to avoid nesting inside already-running loop
    # Use to_thread if available, otherwise run directly via sync helper (fresh loop not nested)
    # Since this is called from asyncio.run context, we cannot create new loop inside running loop via run_until_complete,
    # so delegate to thread
    return await asyncio.to_thread(_loop_shutdown_sync)


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
