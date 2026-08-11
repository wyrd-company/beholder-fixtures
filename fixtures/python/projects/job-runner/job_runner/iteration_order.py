"""Ordering and mutation during iteration (PY-CAN-FLOW-007)."""

from __future__ import annotations


def dict_insertion_order() -> list[str]:
    """Dict preserves insertion order (Python 3.7+)."""
    job_order: dict[str, int] = {}
    job_order["first"] = 1
    job_order["second"] = 2
    job_order["third"] = 3
    return list(job_order.keys())


def dict_replacement_preserves_order() -> list[str]:
    """Replacing value for existing key does not change order."""
    job_order: dict[str, int] = {"alpha": 1, "beta": 2, "gamma": 3}
    job_order["beta"] = 99  # replacement
    return list(job_order.keys())


def dict_value_replacement() -> dict[str, int]:
    """Value replacement with same key updates value."""
    data: dict[str, int] = {"job-a": 1}
    data["job-a"] = 2
    data["job-a"] = 3
    return data


def dict_deletion_and_reinsertion() -> list[str]:
    """Deleting and reinserting moves key to end."""
    data: dict[str, int] = {"a": 1, "b": 2, "c": 3}
    del data["b"]
    data["b"] = 22
    return list(data.keys())


def dict_size_failure_during_iteration() -> str:
    """Mutating dict size during iteration raises RuntimeError."""
    data: dict[str, int] = {"a": 1, "b": 2, "c": 3}
    try:
        for key in data:
            if key == "a":
                data["d"] = 4
    except RuntimeError as exc:
        return f"size-failure-{type(exc).__name__}"
    return "no-failure"


def unordered_set_iteration() -> dict[str, object]:
    """Set iteration order is not guaranteed; do not assert exact order."""
    job_tags = {"urgent", "batch", "retry"}
    # Only assert membership, not order
    seen = set()
    for tag in job_tags:
        seen.add(tag)
    return {
        "members": sorted(seen),
        "count": len(seen),
        "order_is_arbitrary": True,
    }


def list_mutation_during_iteration() -> list[int]:
    """List mutation during iteration has defined but subtle behavior."""
    # Modifying list during iteration does not raise but interacts with index
    items = [1, 2, 3, 4]
    result: list[int] = []
    for value in items:
        result.append(value)
        if value == 2:
            items.append(5)
    return result


def list_mutation_with_index_note() -> str:
    """Note: inserting/removing during iteration affects subsequent iteration."""
    items = [1, 2, 3]
    visited: list[int] = []
    for value in list(items):  # iterate over snapshot to avoid mutation hazard
        visited.append(value)
        if value == 1:
            items.insert(0, 0)
    return f"visited-{visited}-final-{items}"


def fixed_vs_random_hash_seed_note() -> str:
    """Hash seed affects set order but not dict insertion order guarantee."""
    # PYTHONHASHSEED=0 or random changes hash randomization, affecting set
    # iteration order but dict insertion order remains guaranteed since 3.7.
    # Alternative implementations may differ; no exact set order asserted.
    return "hash-seed-affects-set-order-not-dict-insertion"


def alternative_implementation_note() -> str:
    """Alternative implementations preserve same language guarantee for dict order."""
    return "dict-order-guaranteed-language-defined-since-3.7"
