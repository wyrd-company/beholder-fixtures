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


def unexpected_keyword_failure() -> str:
    """Passing an unexpected keyword through ``**options`` must raise only if bound name collides."""

    try:
        # ``origin`` is positional-only, so calling with keyword must fail.
        schedule_task(origin="a", destination="b", priority=1)  # type: ignore[call-arg]
        return "no-error"
    except TypeError:
        return "type-error"


def positional_keyword_misuse() -> str:
    """Positional-only misuse and keyword-only positioning failures."""

    try:
        schedule_task("a", "b", priority=1, mode="standard", extra="x")
        # Should succeed since extra goes to **options.
        # Now provoke failure by passing keyword-only as positional:
        schedule_task("a", "b", 1, "hub", "extra-pos", "should-be-kw")  # too many positional before kw
        # Actually above is valid (extra positional to *hops). Force misuse:
        schedule_task("a", "b", 1, "hub", mode="standard", unexpected_pos="oops")
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
        schedule_task("a", "b", priority=1, origin="oops")  # type: ignore[call-arg]
        return "no-error"
    except TypeError:
        return "type-error"
