"""Exception-target lifetime (PY-CAN-BIND-006)."""

from __future__ import annotations

import sys


def handler_target_lifetime() -> tuple[str, str]:
    """Shadow an existing name with `except ... as target` and release it."""

    marker = "before-handler"
    observed: list[str] = []

    try:
        raise ValueError("settings conflict")
    except ValueError as marker:
        observed.append(marker.args[0])
    finally:
        after = marker

    observed.append(after)
    return observed[0], observed[1]


def ordinary_block_scope() -> str:
    """Contrast exception handlers with ordinary compound statements that share scope."""

    if True:
        block_binding = "inside-if"
    after = block_binding
    return after


def exception_group_subgroup() -> list[str]:
    """Bind subgroups from an exception group handler."""

    if sys.version_info < (3, 11):
        return []

    collected: list[str] = []
    group = ExceptionGroup(
        "bundle",
        [ValueError("alpha"), TypeError("beta")],
    )

    try:
        raise group
    except* ValueError as subgroup:
        collected.extend(str(error) for error in subgroup.exceptions)

    return collected


def retained_traceback_reference() -> str | None:
    """Retain a traceback object after the handler completes."""

    reference = None

    try:
        raise RuntimeError("retained")
    except RuntimeError as error:
        reference = error.__traceback__

    if reference is None:
        return None
    return reference.tb_frame.f_code.co_name
