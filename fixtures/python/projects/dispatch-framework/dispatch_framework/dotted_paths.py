"""Dotted-path references (PY-CAN-DYN-004)."""

from __future__ import annotations

import importlib
import logging
import logging.config
from unittest import mock


class LoaderError(RuntimeError):
    pass


# Dot versus colon grammar: both forms are accepted.
def resolve_dotted_path(path: str) -> object:
    """Resolve 'a.b.c', 'a.b:c', or 'a.b.c:d' style references."""
    colon_parts = path.split(":")
    if len(colon_parts) == 2:
        module_part, attr_part = colon_parts
        full = f"{module_part}.{attr_part}" if attr_part else module_part
    elif len(colon_parts) == 1:
        full = path
    else:
        raise LoaderError(f"malformed path: {path!r}")
    # String composition variant: path built from fragments.
    segments = full.rsplit(".", 1)
    if len(segments) == 1:
        return importlib.import_module(full)
    mod_name, attr_name = segments
    try:
        module = importlib.import_module(mod_name)
    except ModuleNotFoundError as exc:
        raise LoaderError(f"missing module {mod_name!r}") from exc
    try:
        return getattr(module, attr_name)
    except AttributeError as exc:
        raise LoaderError(f"missing attribute {attr_name!r} in {mod_name!r}") from exc


def build_composed_path(base: str, name: str, use_colon: bool = False) -> str:
    """Build a dotted path from pieces (string composition)."""
    if use_colon:
        return f"{base}:{name}"
    return f"{base}.{name}"


# Local factory: resolves short names and dotted paths against a local table plus import fallback.
_FACTORY_TABLE: dict[str, object] = {}


def factory_register(name: str, target: object) -> None:
    _FACTORY_TABLE[name] = target


def factory_create(path: str, *args: object, **kwargs: object) -> object:
    if path in _FACTORY_TABLE:
        target = _FACTORY_TABLE[path]
    else:
        target = resolve_dotted_path(path)
    if callable(target):
        return target(*args, **kwargs)
    return target


# Stale rename counterexample: old path no longer resolves.
STALE_PATH = "dispatch_framework.dotted_paths.OldHandlerName"


def try_stale_path() -> tuple[bool, str]:
    try:
        resolve_dotted_path(STALE_PATH)
        return True, "resolved"
    except LoaderError as exc:
        return False, str(exc)


# Mock patching variant: patch where looked up, not where defined.
def produce_value() -> str:
    return "real"


def patched_demo() -> str:
    # Patch the defining module (straightforward case).
    with mock.patch("dispatch_framework.dotted_paths.produce_value", return_value="mocked"):
        return produce_value()


def patch_where_looked_up_demo() -> str:
    # Consumer imports produce_value; patch the consumer binding, not the defining module.
    import dispatch_framework.consumer as consumer

    # Correct: patch where looked up (consumer), not where defined.
    with mock.patch("dispatch_framework.consumer.consumed_value", return_value="patched-consumer"):
        via_consumer = consumer.consume_value()
        via_defining = produce_value()
    # Contrast: patching defining module alone does not affect already-imported consumer binding.
    with mock.patch("dispatch_framework.dotted_paths.produce_value", return_value="patched-defining"):
        still_consumer = consumer.consume_value()
        patched_defining = produce_value()
    via_path = resolve_dotted_path("dispatch_framework.dotted_paths.produce_value")
    return f"{via_consumer}:{via_defining}:{still_consumer}:{patched_defining}:{callable(via_path)}"


# Logging configuration via dotted logger name.
def configure_logging_via_dotted_path(level: str = "INFO") -> logging.Logger:
    """Configure a dotted logger through dictConfig (logging dotted-path convention)."""
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "mem": {"class": "logging.NullHandler"},
        },
        "loggers": {
            "dispatch_framework": {"level": level, "handlers": ["mem"], "propagate": False},
            "dispatch_framework.dotted_paths": {"level": level, "handlers": ["mem"], "propagate": False},
        },
    }
    logging.config.dictConfig(config)
    return logging.getLogger("dispatch_framework.dotted_paths")


# Register some factory entries.
class CatalogWidget:
    def __init__(self, label: str = "widget") -> None:
        self.label = label


factory_register("widget", CatalogWidget)
factory_register("produce_value", produce_value)
