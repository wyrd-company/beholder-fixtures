"""Parameter kinds and call binding (PY-CAN-CALL-001)."""

from __future__ import annotations


def schedule_task(
    origin: str,
    destination: str,
    /,
    priority: int,
    *hops: str,
    mode: str = "standard",
    **options: str,
) -> dict[str, object]:
    """Define one callable with every parameter kind.

    - ``origin`` and ``destination`` are positional-only (``/``).
    - ``priority`` is positional-or-keyword.
    - ``*hops`` is variadic positional.
    - ``mode`` is keyword-only with a default.
    - ``**options`` is variadic keyword.
    """

    return {
        "origin": origin,
        "destination": destination,
        "priority": priority,
        "hops": list(hops),
        "mode": mode,
        "options": dict(options),
    }


def valid_unpacking_variants() -> list[dict[str, object]]:
    """Exercise valid unpacking of positional and keyword arguments."""

    args = ["north", "south"]
    extra_hops = ["hub-a", "hub-b"]
    kw = {"mode": "express", "channel": "parcel"}

    baseline = schedule_task("north", "south", 2, *extra_hops, **kw)
    from_iterable = schedule_task(*args, 1, *extra_hops, **kw)
    mixed = schedule_task(*args, 3, *extra_hops, **{"mode": "bulk"})
    full_unpack = schedule_task(*args, 5, *extra_hops, **kw)
    return [baseline, from_iterable, mixed, full_unpack]


def duplicate_keyword_failure() -> str:
    """Duplicate keyword binding via unpacking must raise ``TypeError``."""

    try:
        schedule_task("a", "b", 1, mode="standard", **{"mode": "express"})  # type: ignore[arg-type]
        return "no-error"
    except TypeError:
        return "type-error"


def missing_required_failure() -> str:
    """Omitting a required positional-or-keyword parameter must raise ``TypeError``."""

    try:
        schedule_task("a", "b")  # type: ignore[call-arg]
        return "no-error"
    except TypeError:
        return "type-error"


def _strict_pos_only(origin: str, destination: str, /, priority: int) -> tuple[str, str, int]:
    """Strict positional-only helper without variadics for failure probes."""

    return origin, destination, priority


def _strict_kw_only(*, mode: str = "standard") -> str:
    """Strict keyword-only helper for misuse probe."""

    return mode


def _strict_no_variadic(origin: str, destination: str, /, priority: int, *, mode: str = "standard") -> tuple[str, str, int, str]:
    """Helper without *hops/**options to surface unexpected-keyword failure."""

    return origin, destination, priority, mode


def unexpected_keyword_failure() -> str:
    """Passing an unexpected keyword to a strict callable must raise ``TypeError``."""

    try:
        _strict_no_variadic("a", "b", 1, mode="standard", extra="x")  # type: ignore[call-arg]
        return "no-error"
    except TypeError:
        return "type-error"


def positional_keyword_misuse() -> str:
    """Positional-only as keyword and keyword-only as positional must both raise."""

    try:
        _strict_pos_only(origin="a", destination="b", priority=1)  # type: ignore[call-arg]
        return "no-error"
    except TypeError:
        pass
    try:
        _strict_kw_only("bulk")  # type: ignore[call-arg]
        return "no-error"
    except TypeError:
        return "type-error"


def builtin_positional_only_contrast() -> str:
    """Contrast user positional-only with a built-in that is positional-only."""

    token = "parcel"
    # ``str`` built-ins like ``len``? Use ``len`` which is positional-only.
    try:
        _ = len(obj=token)  # type: ignore[call-arg]
        return "no-error"
    except TypeError:
        return "type-error"


def positional_only_via_keyword_probe() -> str:
    """Calling a positional-only parameter by keyword must raise ``TypeError``."""

    try:
        _strict_pos_only(origin="a", destination="b", priority=1)  # type: ignore[call-arg]
        return "no-error"
    except TypeError:
        return "type-error"
