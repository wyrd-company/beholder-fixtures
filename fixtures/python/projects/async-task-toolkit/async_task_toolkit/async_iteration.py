"""Asynchronous iteration and generators (PY-CAN-CALL-013)."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any


class ParcelAsyncIterator:
    """Custom async iterator yielding parcel labels."""

    def __init__(self, labels: list[str]) -> None:
        self._labels = labels
        self._index = 0

    def __aiter__(self) -> AsyncIterator[str]:
        return self

    async def __anext__(self) -> str:
        if self._index >= len(self._labels):
            raise StopAsyncIteration
        await asyncio.sleep(0)
        label = self._labels[self._index]
        self._index += 1
        return f"iter:{label}"


async def parcel_async_generator(count: int) -> AsyncGenerator[str, None]:
    """Async generator that yields labels and supports cleanup via ``aclose``."""

    try:
        for idx in range(count):
            await asyncio.sleep(0)
            yield f"ag:{idx}"
    finally:
        await asyncio.sleep(0)


async def async_comprehension(labels: list[str]) -> list[str]:
    """Async comprehension over an async generator."""

    return [item.upper() async for item in parcel_async_generator(len(labels))]


async def early_exit() -> dict[str, object]:
    """Early ``break`` from ``async for`` with explicit ``aclose`` to run finalization hooks."""

    cleanup: list[str] = []

    async def tracked() -> AsyncGenerator[str, None]:
        try:
            for idx in range(5):
                yield f"tracked:{idx}"
        finally:
            cleanup.append("finalized")

    gen = tracked()
    collected: list[str] = []
    async for item in gen:
        collected.append(item)
        if len(collected) == 2:
            break
    await gen.aclose()
    return {"collected": collected, "cleanup": list(cleanup)}


async def aclose_cleanup() -> list[str]:
    """Explicit ``aclose`` triggers the async generator's ``finally``."""

    events: list[str] = []

    async def gen() -> AsyncGenerator[str, None]:
        try:
            yield "first"
            yield "second"
        finally:
            events.append("closed")

    g = gen()
    assert await g.__anext__() == "first"
    await g.aclose()
    return list(events)


async def stop_async_iteration() -> str:
    """``StopAsyncIteration`` terminates async iteration."""

    iterator = ParcelAsyncIterator(["a", "b"])
    items: list[str] = []
    async for item in iterator:
        items.append(item)
    try:
        await iterator.__anext__()
        return "no-error"
    except StopAsyncIteration:
        return f"stopped:{items}"


def no_async_generator_return_value() -> str:
    """Async generators cannot return a value; ``return x`` is a syntax restriction.

    This function documents the variant by showing a normal async generator
    whose ``StopAsyncIteration`` carries no value.
    """

    async def gen() -> AsyncGenerator[str, None]:
        yield "one"
        # No ``return <value>`` — Python raises SyntaxError if a value is returned.

    async def collect() -> list[str]:
        return [item async for item in gen()]

    return str(asyncio.run(collect()))


async def obsolete_awaitable_aiter() -> dict[str, str]:
    """Legacy awaitable ``__aiter__`` versus modern direct async iterator.

    The modern protocol returns an ``AsyncIterator`` directly. The obsolete
    form returned an awaitable coroutine; on this interpreter it is rejected
    with ``TypeError`` because the coroutine does not implement ``__anext__``.
    """

    class Modern:
        def __aiter__(self) -> AsyncIterator[str]:  # type: ignore[override]
            return ParcelAsyncIterator(["legacy"])

    class LegacyAwaitable:
        def __aiter__(self):  # type: ignore[no-untyped-def]
            async def _get_iter() -> AsyncIterator[str]:
                return ParcelAsyncIterator(["legacy"])

            return _get_iter()

    modern_items: list[str] = []
    async for item in Modern():
        modern_items.append(item)

    try:
        async for _ in LegacyAwaitable():  # type: ignore[call-arg]
            pass
        legacy_result = "no-error"
    except TypeError as exc:
        legacy_result = f"type-error:{exc}"

    return {"modern": ",".join(modern_items), "legacy": legacy_result}


def async_iteration_variants() -> dict[str, object]:
    """Run all async iteration variants and collect results."""

    async def run() -> dict[str, object]:
        iterator = ParcelAsyncIterator(["x", "y"])
        iter_items = [item async for item in iterator]
        agen_items = [item async for item in parcel_async_generator(3)]
        comp = await async_comprehension(["p", "q"])
        early = await early_exit()
        stopped = await stop_async_iteration()
        return {
            "iterator": iter_items,
            "generator": agen_items,
            "comprehension": comp,
            "early": early,
            "stopped": stopped,
        }

    return asyncio.run(run())


async def finalization_hooks() -> dict[str, list[str]]:
    """Exercise async-generator finalization hooks via ``sys.set_asyncgen_hooks``."""

    import gc
    import sys

    hook_events: list[str] = []
    events: list[str] = []

    def firstiter(agen: AsyncGenerator[Any, Any]) -> None:
        hook_events.append("firstiter")

    def finalizer(agen: AsyncGenerator[Any, Any]) -> None:
        hook_events.append("finalizer")

    prev = sys.get_asyncgen_hooks()
    sys.set_asyncgen_hooks(firstiter=firstiter, finalizer=finalizer)
    try:
        # Hook interaction: firstiter on first asend, finalizer on GC of abandoned generator.
        async def hook_gen() -> AsyncGenerator[str, None]:
            try:
                yield "hook-ready"
            finally:
                hook_events.append("hook-finally")

        hg = hook_gen()
        assert await hg.asend(None) == "hook-ready"
        # Abandon without aclose so finalizer hook fires on collection.
        del hg
        gc.collect()
        await asyncio.sleep(0)

        async def gen() -> AsyncGenerator[str, None]:
            try:
                value = yield "ready"
                events.append(f"sent:{value}")
                yield "after"
            except ValueError as exc:
                events.append(f"thrown:{exc}")
                yield "recovered"
            finally:
                events.append("finalized")

        g = gen()
        assert await g.asend(None) == "ready"
        assert await g.asend("parcel") == "after"
        recovered = await g.athrow(ValueError("oops"))
        assert recovered == "recovered"
        await g.aclose()
        await asyncio.sleep(0)
    finally:
        sys.set_asyncgen_hooks(*prev)
    return {"events": list(events), "hooks": list(hook_events)}
