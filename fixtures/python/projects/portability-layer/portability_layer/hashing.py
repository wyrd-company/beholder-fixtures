"""Hash randomization and unordered output (PY-CAN-PLAT-009)."""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum


class HashSeedMode(str, Enum):
    RANDOM = "random"
    FIXED = "42"
    DISABLED = "0"


@dataclass(frozen=True)
class HashRun:
    seed: str
    hash_value: int
    dict_order: list[str]
    set_serialized: str


def _child_code() -> str:
    return (
        "import os, json; "
        "keys=['delta','alpha','charlie','bravo']; "
        "d={k: hash(k) for k in keys}; "
        "print('hash_alpha=' + str(hash('alpha'))); "
        "print('dict_keys=' + ','.join(d.keys())); "
        "print('sorted_keys=' + ','.join(sorted(d.keys()))); "
        "s={'zebra','apple','mango'}; "
        "print('set_sorted=' + ','.join(sorted(s))); "
        "print('seed=' + str(os.environ.get('PYTHONHASHSEED'))); "
    )


def run_under_seed(seed: str) -> subprocess.CompletedProcess[str]:
    """Run a child under a specific PYTHONHASHSEED value.

    Covers random, fixed, and disabled (0) hash seed variants via child process
    / interpreter flags context.
    """
    env = os.environ.copy()
    env["PYTHONHASHSEED"] = seed
    return subprocess.run(
        [sys.executable, "-c", _child_code()],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def deterministic_hash_report() -> dict[str, HashRun]:
    """Compare child runs and show deterministic sorted output."""
    r_random = run_under_seed(HashSeedMode.RANDOM.value)
    r_fixed = run_under_seed(HashSeedMode.FIXED.value)
    r_disabled = run_under_seed(HashSeedMode.DISABLED.value)

    def parse(proc: subprocess.CompletedProcess[str], label: str) -> HashRun:
        lines = proc.stdout.strip().splitlines()
        vals = {k: v for k, v in (line.split("=", 1) for line in lines if "=" in line)}
        return HashRun(
            seed=label,
            hash_value=int(vals.get("hash_alpha", "0")),
            dict_order=vals.get("dict_keys", "").split(",") if vals.get("dict_keys") else [],
            set_serialized=vals.get("set_sorted", ""),
        )

    return {
        "random": parse(r_random, HashSeedMode.RANDOM.value),
        "fixed": parse(r_fixed, HashSeedMode.FIXED.value),
        "disabled": parse(r_disabled, HashSeedMode.DISABLED.value),
    }


def sorted_serialization(items: list[str]) -> str:
    """Deterministic serialization via sorted output.

    Dict insertion order is preserved, but deterministic output requires sorting.
    This function is the canonical pattern: never rely on set/dict iteration order
    for serialized output; sort explicitly.
    """
    return ",".join(sorted(items))


def demonstrate_order_stability() -> dict[str, object]:
    """Show dict insertion order remains while set order needs sorting."""
    insertion = {}
    for key in ["delta", "alpha", "charlie", "bravo"]:
        insertion[key] = len(key)
    inserted_keys = list(insertion.keys())
    sample_set = {"zebra", "apple", "mango"}
    unsorted = list(sample_set)
    sorted_out = sorted_serialization(list(sample_set))
    child_report = deterministic_hash_report()
    # Sorted output is identical across seeds: the deterministic serialization claim.
    sorted_consistent = (
        child_report["random"].set_serialized
        == child_report["fixed"].set_serialized
        == child_report["disabled"].set_serialized
        == "apple,mango,zebra"
    )
    return {
        "insertion_order": inserted_keys,
        "set_unsorted_sample": unsorted,
        "set_sorted": sorted_out,
        "child_report": child_report,
        "sorted_consistent": sorted_consistent,
    }
