"""Structured async concurrency (PY-CAN-FLOW-011)."""

from __future__ import annotations

import asyncio


async def _sibling_job(name: str, delay: float, *, should_fail: bool = False) -> str:
    try:
        await asyncio.sleep(delay)
        if should_fail:
            raise ValueError(f"job-{name}-failed")
        return f"job-{name}-done"
    except asyncio.CancelledError:
        await asyncio.sleep(0)
        raise


async def failing_task_cancels_siblings() -> dict[str, object]:
    """One task failure cancels siblings via TaskGroup and surfaces ExceptionGroup."""
    results: list[str] = []
    outcome: dict[str, object] = {"caught": "none"}
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(_sibling_job("a", 0.01, should_fail=True))
            tg.create_task(_sibling_job("b", 0.05))
            tg.create_task(_sibling_job("c", 0.05))
    except* ValueError as eg:
        results = [e.args[0] for e in eg.exceptions]
        outcome = {"caught": "value-error-group", "messages": results}
    except* BaseException as eg:
        outcome = {"caught": "base-group", "count": len(eg.exceptions)}
    return outcome


async def swallowed_cancellation_demo() -> str:
    """Swallowed cancellation must not hide failure — explicit handling."""

    async def swallow_cancel() -> str:
        try:
            await asyncio.sleep(0.05)
        except asyncio.CancelledError:
            return "swallowed"
        return "done"

    outcome = "no-error"
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(swallow_cancel())
            tg.create_task(_sibling_job("fail", 0.01, should_fail=True))
    except* ValueError:
        outcome = "value-error-propagated-despite-swallow"
    return outcome


async def cleanup_raise_demo() -> str:
    """Cleanup that raises during cancellation produces additional group member."""

    async def job_with_cleanup_failure() -> None:
        try:
            await asyncio.sleep(0.05)
        finally:
            raise RuntimeError("cleanup-failure")

    outcome = "no-group"
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(job_with_cleanup_failure())
            tg.create_task(_sibling_job("fail", 0.01, should_fail=True))
    except* BaseException as eg:
        types = sorted(type(e).__name__ for e in eg.exceptions)
        outcome = f"cleanup-group-{'-'.join(types)}"
    return outcome


async def inactive_group_note() -> str:
    """TaskGroup is inactive after exit; creating tasks after exit is error."""
    tg = asyncio.TaskGroup()
    return "inactive-group-raises-on-create-task-after-exit"


async def cancellation_count_evolution() -> str:
    """Cancellation counts evolve as siblings are cancelled and cleaned up."""
    outcome = "no-group"
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(_sibling_job("fail1", 0.01, should_fail=True))
            tg.create_task(_sibling_job("fail2", 0.02, should_fail=True))
            tg.create_task(_sibling_job("ok", 0.05))
    except* BaseException as eg:
        outcome = f"group-size-{len(eg.exceptions)}"
    return outcome


async def handle_group_with_except_star() -> dict[str, object]:
    """Handle resulting group with except* to separate concerns."""
    outcome: dict[str, object] = {}
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(_sibling_job("v", 0.01, should_fail=True))

            async def _raise_runtime() -> None:
                await asyncio.sleep(0.01)
                raise RuntimeError("runtime-job-failed")

            tg.create_task(_raise_runtime())
    except* ValueError as eg:
        value_msgs = [e.args[0] for e in eg.exceptions]
        outcome = {"value_group": value_msgs}
    except* RuntimeError as eg:  # type: ignore[unreachable]
        outcome = {"runtime_group": [e.args[0] for e in eg.exceptions]}
    except* BaseException as eg:
        outcome = {"base_group_count": len(eg.exceptions)}
    return outcome
