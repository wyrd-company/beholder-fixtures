"""Asynchronous iteration and generators (PY-CAN-CALL-013)."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, AsyncIterator


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


async def obsolete_awaitable_aiter() -> str:
    """An ``__aiter__`` that returns an awaitable is legacy; current form returns an async iterator.

    Demonstrate the modern correct form and note the obsolete spelling.
    """

    class Legacy:
        def __aiter__(self):  # type: ignore[no-untyped-def]
            # Modern: should return AsyncIterator directly, not awaitable.
            return ParcelAsyncIterator(["legacy"])

    items: list[str] = []
    async for item in Legacy():  # type: ignore[call-arg]
        items.append(item)
    return ",".join(items)


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


async def finalization_hooks() -> list[str]:
    """Exercise finalization hooks via ``asend``/``aclose``/``athrow``."""

    events: list[str] = []

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
    try:
        await g.athrow(ValueError("oops"))
    except StopAsyncIteration:
        pass
    return list(events)
