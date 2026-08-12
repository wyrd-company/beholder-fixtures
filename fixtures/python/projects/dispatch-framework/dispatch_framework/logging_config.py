"""Module-name-coupled logging (PY-CAN-DYN-013)."""

from __future__ import annotations

import logging
import logging.config

# Module-name-coupled logger children.
logger = logging.getLogger(__name__)
child_logger = logging.getLogger(f"{__name__}.worker")
sub_child = logging.getLogger(f"{__name__}.worker.subtask")


def get_child_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"{__name__}.{name}")


def emit_examples() -> None:
    logger.info("dispatch framework info")
    child_logger.debug("worker debug")
    sub_child.warning("subtask warning")


def configure_external(level: str = "DEBUG") -> None:
    """Configure dotted logger externally (simulates app-level config)."""
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"plain": {"format": "%(name)s:%(levelname)s:%(message)s"}},
        "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "plain"}},
        "loggers": {
            "dispatch_framework": {"level": level, "handlers": ["console"], "propagate": False},
            "dispatch_framework.logging_config": {"level": level, "handlers": ["console"], "propagate": False},
            "dispatch_framework.logging_config.worker": {"level": level, "handlers": ["console"], "propagate": False},
        },
    }
    logging.config.dictConfig(config)


# Rename/move changes identity variant: logger name is tied to __name__.
def logger_name_for(module_name: str) -> str:
    return logging.getLogger(module_name).name


# __main__ changes tree variant.
def main_logger_name() -> str:
    # When module is executed as __main__, getLogger(__name__) becomes " __main__".
    return logging.getLogger("__main__").name


# Propagation / duplicate handlers variant: child propagates to parent, both have handlers.
def propagation_demo() -> tuple[bool, int]:
    parent = logging.getLogger("dispatch_framework")
    child = logging.getLogger("dispatch_framework.logging_config.worker")
    # Propagation defaults to True unless configured False.
    propagates = child.propagate
    handler_count = len(child.handlers) + len(parent.handlers)
    return propagates, handler_count


def propagation_duplicate_demo() -> tuple[int, int, bool]:
    parent = logging.getLogger("dispatch_framework")
    child = logging.getLogger("dispatch_framework.logging_config.worker")
    parent.handlers.clear()
    child.handlers.clear()
    parent.addHandler(logging.NullHandler())
    child.addHandler(logging.NullHandler())
    child.propagate = True
    # With propagate True, a record emitted by child is handled by child's handler plus parent's via propagation.
    # Effective handler walk: child.handlers + (parent.handlers if propagate else [])
    child_handler_count = len(child.handlers)
    parent_handler_count = len(parent.handlers)
    emits_to_both = child.propagate and parent_handler_count > 0 and child_handler_count > 0
    duplicate_path = emits_to_both
    total_effective = child_handler_count + (parent_handler_count if child.propagate else 0)
    return child_handler_count, parent_handler_count, duplicate_path


# Import-time configuration: executed at import time, then external config conflicts.
_import_time_config_applied = False
_import_time_handler: logging.Handler | None = None


def _apply_import_time_config() -> None:
    global _import_time_config_applied, _import_time_handler
    if not _import_time_config_applied:
        cfg = {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {"early": {"class": "logging.NullHandler"}},
            "loggers": {"dispatch_framework.logging_config": {"level": "INFO", "handlers": ["early"], "propagate": False}},
        }
        logging.config.dictConfig(cfg)
        _import_time_config_applied = True
        # Keep reference for conflict check.
        _import_time_handler = logging.getLogger("dispatch_framework.logging_config").handlers[0] if logging.getLogger("dispatch_framework.logging_config").handlers else None


# Execute at import time.
_apply_import_time_config()


def import_time_conflict_demo() -> tuple[bool, list[str], list[str], bool]:
    """Show import-time config conflicts with external configuration."""
    before_handlers = logging.getLogger("dispatch_framework.logging_config").handlers[:]
    before_types = [type(h).__name__ for h in before_handlers]
    before_has_early = "NullHandler" in before_types
    # External configuration replaces the import-time NullHandler with StreamHandler.
    configure_external(level="INFO")
    after_handlers = logging.getLogger("dispatch_framework.logging_config").handlers[:]
    after_types = [type(h).__name__ for h in after_handlers]
    # Conflict: early NullHandler is replaced by StreamHandler from external config.
    conflict = before_has_early and "StreamHandler" in after_types and "NullHandler" not in after_types
    return before_has_early, before_types, after_types, conflict


_CONFIGURED = False


def ensure_configured() -> bool:
    global _CONFIGURED
    if not _CONFIGURED:
        _CONFIGURED = True
        return False
    return True
