"""Time zones and clocks (PY-CAN-PLAT-006)."""

from __future__ import annotations

import os
import pathlib
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, available_timezones


@dataclass(frozen=True)
class ClockComparison:
    wall: float
    monotonic: float
    wall_again: float


@dataclass(frozen=True)
class AmbiguousWallTime:
    naive: datetime
    aware_first: datetime
    aware_second: datetime
    fold_values: tuple[int, int]


@dataclass(frozen=True)
class TimestampPrecision:
    requested_ns: int
    observed_ns: int
    non_exact: bool


def aware_and_naive_values() -> dict[str, object]:
    """Demonstrate aware versus naive datetime values."""
    naive = datetime(2024, 6, 15, 12, 0, 0)
    aware_utc = datetime(2024, 6, 15, 12, 0, 0, tzinfo=timezone.utc)
    eastern = ZoneInfo("America/New_York")
    aware_eastern = datetime(2024, 6, 15, 12, 0, 0, tzinfo=eastern)
    # Convert aware to UTC
    converted = aware_eastern.astimezone(timezone.utc)
    return {
        "naive": naive,
        "naive_has_tz": naive.tzinfo is not None,
        "aware_utc": aware_utc,
        "aware_eastern": aware_eastern,
        "converted_utc": converted,
        "is_aware": lambda dt: dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None,  # noqa: E731
    }


def ambiguous_fold_example() -> AmbiguousWallTime:
    """Create an ambiguous wall time via DST fold (PEP 495).

    Uses America/New_York DST end 2024-11-03 where 01:30 occurs twice.
    """
    tz = ZoneInfo("America/New_York")
    # First occurrence (DST, fold=0)
    first = datetime(2024, 11, 3, 1, 30, 0, tzinfo=tz, fold=0)
    # Second occurrence (standard, fold=1)
    second = datetime(2024, 11, 3, 1, 30, 0, tzinfo=tz, fold=1)
    naive = datetime(2024, 11, 3, 1, 30, 0)
    # Offsets differ
    off_first = first.utcoffset()
    off_second = second.utcoffset()
    _ = (off_first, off_second)
    return AmbiguousWallTime(
        naive=naive,
        aware_first=first,
        aware_second=second,
        fold_values=(first.fold, second.fold),
    )


def monotonic_vs_wall() -> ClockComparison:
    """Capture monotonic versus wall clock readings."""
    wall_before = time.time()
    mono = time.monotonic()
    wall_after = time.time()
    # Also capture perf_counter and process_time as related clocks
    _perf = time.perf_counter()
    _proc = time.process_time()
    _ = (_perf, _proc)
    return ClockComparison(wall=wall_before, monotonic=mono, wall_again=wall_after)


def timestamp_precision_probe() -> TimestampPrecision:
    """Show non-exact file timestamp precision on this filesystem."""
    with tempfile.TemporaryDirectory() as td:
        p = pathlib.Path(td) / "probe.txt"
        p.write_text("x", encoding="utf-8")
        # Request a timestamp with nanosecond precision that filesystem may truncate.
        # Use utime_ns with an odd nanosecond value unlikely to be stored exactly on all FS.
        requested = 1_700_000_000_123_456_789
        try:
            os.utime(p, ns=(requested, requested))
            observed = p.stat().st_mtime_ns
            non_exact = observed != requested
        except OSError:
            observed = p.stat().st_mtime_ns
            non_exact = False
        return TimestampPrecision(requested_ns=requested, observed_ns=observed, non_exact=non_exact)


def zoneinfo_availability() -> dict[str, object]:
    """Show system zoneinfo database availability without vendoring."""
    zones = available_timezones()
    has_ny = "America/New_York" in zones
    has_utc = "UTC" in zones
    now_ny = datetime.now(tz=ZoneInfo("America/New_York"))
    now_utc = datetime.now(tz=timezone.utc)
    return {
        "count": len(zones),
        "has_ny": has_ny,
        "has_utc": has_utc,
        "now_ny": now_ny,
        "now_utc": now_utc,
        "system_db_present": has_ny and has_utc,
    }


def demonstrate_clocks() -> dict[str, object]:
    fold = ambiguous_fold_example()
    return {
        "aware_naive": aware_and_naive_values(),
        "fold": fold,
        "fold_offsets_differ": fold.aware_first.utcoffset() != fold.aware_second.utcoffset(),
        "monotonic": monotonic_vs_wall(),
        "precision": timestamp_precision_probe(),
        "zones": zoneinfo_availability(),
        "timedelta_example": timedelta(hours=1),
    }
