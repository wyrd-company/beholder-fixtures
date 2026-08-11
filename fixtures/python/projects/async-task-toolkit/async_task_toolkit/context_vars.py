"""Context variables (PY-CAN-CALL-014)."""

from __future__ import annotations

import asyncio
import contextvars
import threading

request_label: contextvars.ContextVar[str] = contextvars.ContextVar("request_label", default="default-label")
parcel_count: contextvars.ContextVar[int] = contextvars.ContextVar("parcel_count", default=0)


async def task_context_capture() -> dict[str, object]:
    """Each task captures its context at creation; mutation does not leak."""

    request_label.set("main")

    async def worker(label: str) -> str:
        await asyncio.sleep(0)
        return request_label.get()

    # Tasks capture context at creation time.
    request_label.set("before-create")
    t1 = asyncio.create_task(worker("t1"))
    request_label.set("after-create")
    t2 = asyncio.create_task(worker("t2"))

    r1 = await t1
    r2 = await t2
    return {"t1": r1, "t2": r2, "main": request_label.get()}


def task_isolation() -> dict[str, str]:
    """Task-local mutation does not propagate to siblings."""

    async def run() -> dict[str, str]:
        request_label.set("root")

        async def child(label: str) -> str:
            request_label.set(label)
            await asyncio.sleep(0)
            return request_label.get()

        results = await asyncio.gather(child("alpha"), child("beta"))
        return {"alpha": results[0], "beta": results[1], "root": request_label.get()}

    return asyncio.run(run())


def nested_propagation() -> list[str]:
    """Nested contexts propagate outward until reset."""

    log: list[str] = []
    var = contextvars.ContextVar("nested_var", default="outer")

    var.set("level-0")
    log.append(var.get())
    token1 = var.set("level-1")
    log.append(var.get())
    token2 = var.set("level-2")
    log.append(var.get())
    var.reset(token2)
    log.append(var.get())
    var.reset(token1)
    log.append(var.get())
    return log


def token_reset_order() -> dict[str, object]:
    """Reset must use the correct token; out-of-order reset is observable."""

    var = contextvars.ContextVar("reset_order_var", default="base")
    base = var.get()
    t1 = var.set("first")
    t2 = var.set("second")
    second = var.get()
    # Correct order: reset t2 then t1.
    var.reset(t2)
    after_t2 = var.get()
    try:
        # Resetting t2 again should fail (token already used).
        var.reset(t2)
        second_reset = "no-error"
    except (ValueError, RuntimeError):
        second_reset = "invalid-token"
    var.reset(t1)
    restored = var.get()
    return {
        "base": base,
        "second": second,
        "after_t2": after_t2,
        "second_reset": second_reset,
        "restored": restored,
    }


def thread_transition() -> dict[str, str]:
    """Explicit cross-thread context propagation via ``Context.run``."""

    var = contextvars.ContextVar("thread_var", default="main-default")
    var.set("main-value")
    ctx = contextvars.copy_context()
    result: dict[str, str] = {}

    def in_thread() -> None:
        # Without explicit context, thread sees default.
        result["without_context"] = var.get()
        # Run with copied context.
        def with_copied() -> None:
            result["with_context"] = var.get()

        ctx.run(with_copied)

    t = threading.Thread(target=in_thread)
    t.start()
    t.join()
    return result


def explicit_cross_thread_context() -> dict[str, str]:
    """Show that ``copy_context`` isolates thread-local modifications."""

    var = contextvars.ContextVar("cross_thread_var", default="origin")
    var.set("origin-value")
    ctx = contextvars.copy_context()
    observed: dict[str, str] = {}

    def worker() -> None:
        var.set("thread-modified")
        observed["thread"] = var.get()

    ctx.run(worker)
    observed["main"] = var.get()
    return observed


def framework_scheduler_context() -> dict[str, str]:
    """Framework-style scheduler that propagates context to each scheduled task."""

    async def run() -> dict[str, str]:
        request_label.set("scheduler-root")
        results: dict[str, str] = {}

        async def job(name: str) -> None:
            await asyncio.sleep(0)
            results[name] = request_label.get()

        # Schedule jobs after setting different labels; each captures at create.
        request_label.set("job-alpha")
        a = asyncio.create_task(job("alpha"))
        request_label.set("job-beta")
        b = asyncio.create_task(job("beta"))
        await asyncio.gather(a, b)
        return results

    return asyncio.run(run())
