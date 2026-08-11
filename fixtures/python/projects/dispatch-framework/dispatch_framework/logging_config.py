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


# Propagation / duplicate handlers variant.
def propagation_demo() -> tuple[bool, int]:
    parent = logging.getLogger("dispatch_framework")
    child = logging.getLogger("dispatch_framework.logging_config.worker")
    # Propagation defaults to True unless configured False.
    propagates = child.propagate
    handler_count = len(child.handlers) + len(parent.handlers)
    return propagates, handler_count


# Import-time config conflict variant: avoid configuring at import time; expose function instead.
# If this module called configure_external() at top level, it would conflict with app config.
_CONFIGURED = False


def ensure_configured() -> bool:
    global _CONFIGURED
    if not _CONFIGURED:
        _CONFIGURED = True
        return False
    return True
