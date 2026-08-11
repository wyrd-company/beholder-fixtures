"""Tracing, profiling, and sys.monitoring (PY-CAN-DIAG-015).

Observes call/line/return/exception/generator/async paths and removes
hooks safely. Coverage-tool arcs are excluded; stdlib tracing and
monitoring carry the item.
"""

from __future__ import annotations

import asyncio
import sys
from types import FrameType
from typing import Any


def _sample_target(x: int) -> int:
    if x < 0:
        raise ValueError("negative")
    total = 0
    for i in range(x):
        total += i
    return total


def _sample_generator(n: int):  # type: ignore[no-untyped-def]
    for i in range(n):
        yield i * 2


async def _sample_async_target(n: int) -> int:
    await asyncio.sleep(0)
    return n * 2


# ---------------------------------------------------------------------------
# sys.settrace variant
# ---------------------------------------------------------------------------


def tracing_demo() -> dict[str, object]:
    """Observe call/line/return/exception via sys.settrace."""

    events: list[tuple[str, str]] = []

    def tracer(frame: FrameType, event: str, arg: Any) -> Any:
        # Only track our sample target to keep output bounded.
        if frame.f_code.co_name in {"_sample_target", "_sample_generator"}:
            events.append((event, frame.f_code.co_name))
        return tracer

    prev = sys.gettrace()
    try:
        sys.settrace(tracer)
        _sample_target(3)
        try:
            _sample_target(-1)
        except ValueError:
            pass
        list(_sample_generator(2))
    finally:
        sys.settrace(prev)

    # Per-thread: tracer is per-thread; removal is safe via restoring previous.
    restored = sys.gettrace() is prev
    return {"events": events, "restored": restored, "has_call": any(e[0] == "call" for e in events)}


# ---------------------------------------------------------------------------
# sys.setprofile variant
# ---------------------------------------------------------------------------


def _sample_with_c_call() -> int:
    return len([1, 2, 3, 4])


def profiling_demo() -> dict[str, object]:
    """Observe call/return/c_call via sys.setprofile."""

    events: list[tuple[str, str]] = []

    def profiler(frame: FrameType, event: str, arg: Any) -> None:
        name = frame.f_code.co_name
        if name in {"_sample_target", "_sample_generator", "_sample_with_c_call", "profiling_demo"}:
            events.append((event, name))
        elif event == "c_call":
            # Capture c_call even if caller filter misses; still record
            events.append((event, name))

    prev = sys.getprofile()
    try:
        sys.setprofile(profiler)
        _sample_target(2)
        _sample_with_c_call()
        len([1, 2, 3])  # explicit C builtin c_call in profiling_demo frame
    finally:
        sys.setprofile(prev)

    restored = sys.getprofile() is prev
    return {"events": events, "restored": restored, "has_c_call": any(e[0] == "c_call" for e in events)}


# ---------------------------------------------------------------------------
# sys.monitoring (PEP 669) variant – Python 3.12+
# ---------------------------------------------------------------------------


def monitoring_demo() -> dict[str, object]:
    """Observe via sys.monitoring (PEP 669) where available."""

    if not hasattr(sys, "monitoring"):
        return {"available": False, "reason": "sys.monitoring not present"}

    monitoring = sys.monitoring  # type: ignore[attr-defined]
    tool_id = None
    # CPython 3.14 uses use_tool_id(tool_id, name); earlier uses use_tool_id(name).
    # Try CPython 3.14 form first: tool ids 0-5, with 3 and 4 typically free.
    for candidate in (3, 4, 5, 0, 1, 2):
        try:
            monitoring.use_tool_id(candidate, "diagnostics.toolkit.monitoring")  # type: ignore[attr-defined]
            tool_id = candidate
            break
        except ValueError:
            continue
        except TypeError:
            # Older API with single arg – fall back.
            try:
                tool_id = monitoring.use_tool_id("diagnostics.toolkit.monitoring")  # type: ignore[attr-defined]
                break
            except Exception:
                return {"available": False, "reason": "no tool id"}
    if tool_id is None:
        # Try single-arg form as last resort.
        try:
            tool_id = monitoring.use_tool_id("diagnostics.toolkit.monitoring")  # type: ignore[attr-defined]
        except Exception as exc:
            return {"available": False, "reason": f"no tool id: {exc}"}
    events: list[str] = []

    def on_py_start(code: Any, instruction_offset: int) -> Any:
        if code.co_name == "_sample_target":
            events.append("PY_START")
        return monitoring.DISABLE  # type: ignore[attr-defined]

    def on_py_return(code: Any, instruction_offset: int, retval: Any) -> Any:
        if code.co_name == "_sample_target":
            events.append("PY_RETURN")
        return monitoring.DISABLE  # type: ignore[attr-defined]

    try:
        monitoring.register_callback(tool_id, monitoring.events.PY_START, on_py_start)  # type: ignore[attr-defined]
        monitoring.register_callback(tool_id, monitoring.events.PY_RETURN, on_py_return)  # type: ignore[attr-defined]
        monitoring.set_events(tool_id, monitoring.events.PY_START | monitoring.events.PY_RETURN)  # type: ignore[attr-defined]
        _sample_target(2)
        _sample_target(3)
    finally:
        # Safe removal: disable events and free tool id.
        try:
            monitoring.set_events(tool_id, 0)  # type: ignore[attr-defined]
        except Exception:
            pass
        try:
            monitoring.free_tool_id(tool_id)  # type: ignore[attr-defined]
        except Exception:
            pass
        try:
            monitoring.register_callback(tool_id, monitoring.events.PY_START, None)  # type: ignore[attr-defined]
            monitoring.register_callback(tool_id, monitoring.events.PY_RETURN, None)  # type: ignore[attr-defined]
        except Exception:
            pass

    return {"available": True, "events": events, "has_start": "PY_START" in events}


def demo_generator_and_async_paths() -> dict[str, object]:
    """Ensure generator and async paths are observable via tracing."""

    events: list[str] = []

    def tracer(frame: FrameType, event: str, arg: Any) -> Any:
        name = frame.f_code.co_name
        if name in {"_sample_generator", "_sample_async_target"}:
            events.append(f"{event}:{name}")
        return tracer

    prev = sys.gettrace()
    try:
        sys.settrace(tracer)
        gen = _sample_generator(3)
        next(gen)
        list(gen)
        asyncio.run(_sample_async_target(5))
    finally:
        sys.settrace(prev)

    return {"events": events, "has_generator": any("generator" in e for e in events)}


def all_tracing_demos() -> dict[str, object]:
    """Collect tracing / profiling / monitoring demos."""

    return {
        "tracing": tracing_demo(),
        "profiling": profiling_demo(),
        "monitoring": monitoring_demo(),
        "generator_async": demo_generator_and_async_paths(),
    }
