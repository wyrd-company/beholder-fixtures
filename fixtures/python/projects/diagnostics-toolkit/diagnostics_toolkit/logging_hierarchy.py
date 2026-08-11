"""Logging hierarchy (PY-CAN-DIAG-016).

Configures parent/child levels, handlers, propagation, filters,
extras, deferred formatting, and exception data without global leakage.
"""

from __future__ import annotations

import io
import logging
from typing import Any


class ToolkitFilter(logging.Filter):
    """Filter that allows only records containing 'allow'."""

    def filter(self, record: logging.LogRecord) -> bool:  # type: ignore[override]
        return "allow" in record.getMessage()


def _make_memory_handler(stream: io.StringIO) -> logging.Handler:
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter("%(name)s:%(levelname)s:%(message)s"))
    return handler


def setup_hierarchy_demo() -> dict[str, object]:
    """Create parent and child loggers with distinct levels."""

    parent = logging.getLogger("diagnostics_toolkit")
    child = logging.getLogger("diagnostics_toolkit.child")
    # Save prior state to avoid leakage.
    prev_parent_level = parent.level
    prev_child_level = child.level
    prev_parent_handlers = list(parent.handlers)
    prev_child_handlers = list(child.handlers)
    prev_propagate = child.propagate
    stream_parent = io.StringIO()
    stream_child = io.StringIO()
    try:
        parent.handlers = []
        child.handlers = []
        parent.setLevel(logging.DEBUG)
        child.setLevel(logging.INFO)
        handler_parent = _make_memory_handler(stream_parent)
        handler_child = _make_memory_handler(stream_child)
        parent.addHandler(handler_parent)
        child.addHandler(handler_child)
        child.propagate = True
        parent.debug("parent allow debug")
        child.debug("child allow debug hidden by level")
        child.info("child allow info")
        child.warning("child allow warning")
        return {
            "parent_output": stream_parent.getvalue(),
            "child_output": stream_child.getvalue(),
            "parent_level": parent.level,
            "child_level": child.level,
        }
    finally:
        parent.handlers = prev_parent_handlers
        child.handlers = prev_child_handlers
        parent.setLevel(prev_parent_level)
        child.setLevel(prev_child_level)
        child.propagate = prev_propagate


def demo_propagation() -> dict[str, object]:
    """Show propagation from child to parent versus suppressed propagation."""

    parent = logging.getLogger("diagnostics_toolkit.prop")
    child = logging.getLogger("diagnostics_toolkit.prop.child")
    prev_parent_handlers = list(parent.handlers)
    prev_child_handlers = list(child.handlers)
    prev_propagate = child.propagate
    stream_parent = io.StringIO()
    stream_child = io.StringIO()
    try:
        parent.handlers = [_make_memory_handler(stream_parent)]
        child.handlers = [_make_memory_handler(stream_child)]
        parent.setLevel(logging.DEBUG)
        child.setLevel(logging.DEBUG)

        child.propagate = True
        child.info("allow propagated")
        propagated_with = stream_parent.getvalue()

        stream_parent.truncate(0)
        stream_parent.seek(0)
        stream_child.truncate(0)
        stream_child.seek(0)

        child.propagate = False
        child.info("allow not propagated")
        propagated_without = stream_parent.getvalue()

        return {
            "with_propagation": "allow propagated" in propagated_with,
            "without_propagation": "allow not propagated" not in propagated_without,
            "child_captured": "allow not propagated" in stream_child.getvalue(),
        }
    finally:
        parent.handlers = prev_parent_handlers
        child.handlers = prev_child_handlers
        child.propagate = prev_propagate


def demo_filter_and_extra() -> dict[str, object]:
    """Filter records and inject extra context."""

    logger = logging.getLogger("diagnostics_toolkit.filter_demo")
    prev_handlers = list(logger.handlers)
    prev_level = logger.level
    stream = io.StringIO()
    try:
        logger.handlers = [_make_memory_handler(stream)]
        logger.setLevel(logging.DEBUG)
        logger.addFilter(ToolkitFilter())
        logger.info("allow this message")
        logger.info("deny this other")
        logger.info("allow with extra", extra={"request_id": "REQ-123"})
        output = stream.getvalue()
        # Extra is available on the record but not in default formatter; inspect via handler records.
        # We capture via custom handler that records extras.
        extras: list[Any] = []

        class CapturingHandler(logging.Handler):
            def emit(self, record: logging.LogRecord) -> None:
                extras.append(getattr(record, "request_id", None))

        cap = CapturingHandler()
        logger.addHandler(cap)
        logger.info("allow second extra", extra={"request_id": "REQ-999"})
        logger.removeHandler(cap)
        return {
            "output": output,
            "filtered_allow": "allow this message" in output,
            "filtered_deny": "deny this other" not in output,
            "extras": extras,
        }
    finally:
        logger.handlers = prev_handlers
        logger.setLevel(prev_level)
        # Remove filter if added
        for f in list(logger.filters):
            logger.removeFilter(f)


def demo_deferred_formatting() -> dict[str, object]:
    """Deferred formatting via %s style avoids eager f-string evaluation."""

    logger = logging.getLogger("diagnostics_toolkit.deferred")
    prev_handlers = list(logger.handlers)
    prev_level = logger.level
    stream = io.StringIO()
    try:
        logger.handlers = [_make_memory_handler(stream)]
        logger.setLevel(logging.DEBUG)
        # Deferred: args are only formatted if the record is emitted.
        expensive_calls = 0

        class Expensive:
            def __str__(self) -> str:
                nonlocal expensive_calls
                expensive_calls += 1
                return "expensive"

        logger.debug("deferred allow %s", Expensive())
        calls_when_enabled = expensive_calls

        # Now disable debug and verify no formatting occurs.
        logger.setLevel(logging.WARNING)
        expensive_calls = 0
        logger.debug("deferred hidden %s", Expensive())
        calls_when_hidden = expensive_calls

        return {
            "calls_when_enabled": calls_when_enabled,
            "calls_when_hidden": calls_when_hidden,
            "no_leak": stream.getvalue().count("deferred") >= 1,
        }
    finally:
        logger.handlers = prev_handlers
        logger.setLevel(prev_level)


def demo_exception_data() -> dict[str, object]:
    """Log exception data with exc_info without leaking handlers."""

    logger = logging.getLogger("diagnostics_toolkit.exception")
    prev_handlers = list(logger.handlers)
    prev_level = logger.level
    stream = io.StringIO()
    try:
        handler = _make_memory_handler(stream)
        logger.handlers = [handler]
        logger.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter("%(message)s %(exc_text)s"))
        try:
            raise ValueError("demo failure")
        except ValueError:
            logger.error("allow exception occurred", exc_info=True)
        output = stream.getvalue()
        return {
            "has_exception": "ValueError" in output and "demo failure" in output,
            "output": output,
        }
    finally:
        logger.handlers = prev_handlers
        logger.setLevel(prev_level)


def demo_no_global_leakage() -> dict[str, object]:
    """Verify no handlers leaked to root after demos."""

    root_handlers_before = list(logging.getLogger().handlers)
    parent_handlers_before = list(logging.getLogger("diagnostics_toolkit").handlers)
    # Run demos that internally cleanup
    setup_hierarchy_demo()
    demo_propagation()
    demo_filter_and_extra()
    demo_deferred_formatting()
    demo_exception_data()
    root_handlers_after = list(logging.getLogger().handlers)
    parent_handlers_after = list(logging.getLogger("diagnostics_toolkit").handlers)
    return {
        "root_leaked": len(root_handlers_after) != len(root_handlers_before),
        "parent_leaked": len(parent_handlers_after) != len(parent_handlers_before),
        "clean": root_handlers_after == root_handlers_before and parent_handlers_after == parent_handlers_before,
    }


def all_logging_demos() -> dict[str, object]:
    """Collect logging hierarchy demos."""

    return {
        "hierarchy": setup_hierarchy_demo(),
        "propagation": demo_propagation(),
        "filter_extra": demo_filter_and_extra(),
        "deferred": demo_deferred_formatting(),
        "exception": demo_exception_data(),
        "no_leak": demo_no_global_leakage(),
    }
