"""Generators (PY-CAN-CALL-010)."""

from __future__ import annotations

from collections.abc import Generator, Iterator


def parcel_stream(count: int) -> Generator[str, str | None, str]:
    """Generator demonstrating deferred start, send, throw, close, cleanup, and return value."""

    try:
        for idx in range(count):
            incoming = yield f"parcel-{idx}"
            if incoming is not None:
                yield f"echo:{incoming}"
    except GeneratorExit:
        yield "cleanup:generator-exit"
        return
    finally:
        # Cleanup hook runs on close or exhaustion.
        pass
    return "stream-complete"


def explicit_return_value() -> str:
    """Capture a generator's explicit ``return`` via ``StopIteration.value``."""

    def with_return() -> Generator[int, None, str]:
        yield 1
        yield 2
        return "done"

    gen = with_return()
    next(gen)
    next(gen)
    try:
        next(gen)
        return "no-error"
    except StopIteration as exc:
        return exc.value  # type: ignore[no-any-return]


def deferred_start() -> dict[str, object]:
    """Calling a generator does not run its body until first iteration."""

    started = False

    def gen() -> Generator[str, None, None]:
        nonlocal started
        started = True
        yield "first"

    g = gen()
    before = started
    next(g)
    after = started
    g.close()
    return {"before": before, "after": after, "is_generator": isinstance(g, Generator)}


def send_throw_close() -> dict[str, object]:
    """Exercise ``send``, ``throw``, and ``close`` plus ``GeneratorExit`` path."""

    log: list[str] = []

    def worker() -> Generator[str, str, None]:
        try:
            while True:
                incoming = yield "ready"
                log.append(f"received:{incoming}")
        except ValueError as exc:
            log.append(f"thrown:{exc}")
            yield "recovered"
        finally:
            log.append("cleanup")

    gen = worker()
    assert next(gen) == "ready"
    sent = gen.send("parcel")
    thrown = gen.throw(ValueError("oops"))
    gen.close()
    return {"sent": sent, "thrown": thrown, "log": list(log)}


def exhausted_state() -> str:
    """Exhausted generator stays exhausted and raises ``StopIteration``."""

    def one_shot() -> Generator[int, None, None]:
        yield 1

    gen = one_shot()
    next(gen)
    try:
        next(gen)
        return "no-error"
    except StopIteration:
        try:
            next(gen)
            return "no-error-second"
        except StopIteration:
            return "stop-iteration"


def reentry_failure() -> str:
    """Re-entering an already-executing generator must raise ``ValueError``."""

    def recursive() -> Generator[str, None, None]:
        # Capture the executing generator and attempt re-entry.
        try:
            next(gen_ref[0])  # type: ignore[arg-type]
        except ValueError as exc:
            yield f"reentry:{exc}"
        yield "exit"

    gen_ref: list[Generator[str, None, None] | None] = [None]
    gen = recursive()
    gen_ref[0] = gen
    first = next(gen)
    second = next(gen)
    return f"{first}|{second}"


def escaped_stopiteration_transformation() -> str:
    """Escaped ``StopIteration`` inside a generator is transformed to ``RuntimeError`` (PEP 479)."""

    def leaky() -> Generator[int, None, None]:
        # Raising StopIteration inside generator should become RuntimeError.
        raise StopIteration("leak")
        yield 1  # noqa: unreachable

    gen = leaky()
    try:
        next(gen)
        return "no-error"
    except RuntimeError as exc:
        cause = exc.__cause__
        return f"runtime-error:cause={type(cause).__name__ if cause else 'none'}"
    except StopIteration:
        return "stop-iteration"


def generator_expression_variant() -> list[int]:
    """Generator expression variant."""

    source = [1, 2, 3, 4]
    genexp = (item * 2 for item in source if item % 2 == 0)
    return list(genexp)


def generator_expression_vs_list() -> dict[str, object]:
    """Contrast generator expression laziness with list comprehension."""

    counter = 0

    def track(value: int) -> int:
        nonlocal counter
        counter += 1
        return value

    gen = (track(v) for v in range(3))
    before = counter
    list(gen)
    after = counter
    return {"before": before, "after": after}
