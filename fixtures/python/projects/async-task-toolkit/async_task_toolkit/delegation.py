"""``yield from`` delegation (PY-CAN-CALL-011)."""

from __future__ import annotations

from collections.abc import Generator, Iterable


def inner_generator(count: int) -> Generator[str, str | None, str]:
    """Subgenerator whose return value is captured by delegation."""

    for idx in range(count):
        incoming = yield f"inner-{idx}"
        if incoming:
            yield f"inner-echo:{incoming}"
    return f"inner-done:{count}"


def plain_iterable() -> Iterable[str]:
    """Plain iterable (non-generator) for delegation contrast."""

    return ["plain-a", "plain-b", "plain-c"]


def delegating_generator(count: int) -> Generator[str, str | None, str]:
    """Delegate to a generator and a plain iterable via ``yield from``."""

    inner_result = yield from inner_generator(count)
    yield f"captured:{inner_result}"
    plain_result = yield from plain_iterable()
    # Plain iterable has no return value; ``yield from`` yields None.
    yield f"plain-sentinel:{plain_result!r}"
    return "delegation-complete"


def capture_subgenerator_return() -> str:
    """Capture the subgenerator ``return`` value through ``yield from``."""

    gen = delegating_generator(2)
    items: list[str] = []
    try:
        while True:
            items.append(next(gen))
    except StopIteration as exc:
        final = exc.value
    return f"items={items}|final={final}"


def send_propagation() -> dict[str, object]:
    """``send`` through ``yield from`` propagates into the subgenerator."""

    def sub() -> Generator[str, str, str]:
        received = yield "sub-ready"
        yield f"sub-received:{received}"
        return "sub-done"

    def delegator() -> Generator[str, str, str]:
        result = yield from sub()
        yield f"delegator-captured:{result}"
        return "delegator-done"

    gen = delegator()
    assert next(gen) == "sub-ready"
    second = gen.send("parcel")
    assert second == "sub-received:parcel"
    third = next(gen)
    try:
        next(gen)
        final = "no-stop"
    except StopIteration as exc:
        final = exc.value
    return {"second": second, "third": third, "final": final}


def throw_propagation() -> dict[str, object]:
    """``throw`` propagates through ``yield from`` into the subgenerator."""

    log: list[str] = []

    def sub() -> Generator[str, None, None]:
        try:
            yield "sub-yield"
        except ValueError as exc:
            log.append(f"caught:{exc}")
            yield "recovered"

    def delegator() -> Generator[str, None, None]:
        yield from sub()
        yield "after"

    gen = delegator()
    next(gen)
    thrown = gen.throw(ValueError("delegation-oops"))
    after = next(gen)
    return {"thrown": thrown, "after": after, "log": log}


def close_propagation() -> list[str]:
    """``close`` propagates and triggers cleanup in the subgenerator."""

    log: list[str] = []

    def sub() -> Generator[str, None, None]:
        try:
            yield "sub"
        finally:
            log.append("sub-cleanup")

    def delegator() -> Generator[str, None, None]:
        try:
            yield from sub()
        finally:
            log.append("delegator-cleanup")

    gen = delegator()
    next(gen)
    gen.close()
    return list(log)


def plain_iterator_limitations() -> dict[str, object]:
    """Plain iterator delegation cannot propagate ``send`` as a value."""

    def delegator() -> Generator[str, None, None]:
        yield from ["a", "b"]

    gen = delegator()
    assert next(gen) == "a"
    # Sending non-None through yield from to a list iterator raises AttributeError
    # because the underlying iterator has no send method.
    try:
        gen.send("ignored")
        send_result = "no-error"
    except AttributeError:
        send_result = "attribute-error"
    return {"send_result": send_result}


def handler_ownership() -> list[str]:
    """Subgenerator owns handling until exhausted; delegator resumes after."""

    trace: list[str] = []

    def sub() -> Generator[str, None, str]:
        trace.append("sub-start")
        yield "sub-yield"
        trace.append("sub-end")
        return "sub-return"

    def delegator() -> Generator[str, None, str]:
        trace.append("delegator-before")
        result = yield from sub()
        trace.append(f"delegator-after:{result}")
        yield "delegator-yield"
        return "delegator-return"

    gen = delegator()
    next(gen)
    next(gen)
    try:
        next(gen)
    except StopIteration:
        pass
    return list(trace)
