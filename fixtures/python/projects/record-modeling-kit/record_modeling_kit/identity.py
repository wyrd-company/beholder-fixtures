"""Identity, equality, hashing, and mutability (PY-CAN-OBJ-016)."""

from __future__ import annotations

import math
from typing import Any


class EqualDistinct:
    def __init__(self, value: int) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EqualDistinct):
            return self.value == other.value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.value)


class UnhashableViaEq:
    """Equality without hash disables hashing."""

    def __eq__(self, other: object) -> bool:
        return isinstance(other, UnhashableViaEq)

    # No __hash__ defined => __hash__ is None


def singleton_checks_demo() -> tuple[bool, bool, bool]:
    a = None
    b = None
    is_none = a is None
    is_singleton = a is b
    # Contrast with equality: two distinct equal objects are not identical.
    o1 = EqualDistinct(5)
    o2 = EqualDistinct(5)
    eq_but_not_identical = (o1 == o2) and (o1 is not o2)
    return is_none, is_singleton, eq_but_not_identical


def hashable_immutable_demo() -> tuple[bool, bool]:
    tup = (1, 2)
    fs = frozenset([1, 2])
    _ = fs
    try:
        hash(tup)
        hashable = True
    except TypeError:
        hashable = False
    try:
        hash([1, 2])  # type: ignore[arg-type]
        unhashable_mutable = False
    except TypeError:
        unhashable_mutable = True
    return hashable, unhashable_mutable


def equality_disables_hash_demo() -> bool:
    return UnhashableViaEq.__hash__ is None


def nan_nonreflexivity_demo() -> tuple[bool, bool]:
    nan = float("nan")
    is_not_equal_to_self = nan != nan
    # math.nan behaves same.
    is_math_nan_not_equal = math.nan != math.nan
    return is_not_equal_to_self, is_math_nan_not_equal


def hash_randomization_note() -> str:
    # Hash randomization is env-controlled; do not assert specific hash values.
    hashes = {hash("key") for _ in range(1)}  # single run
    return f"hash-is-int:{isinstance(next(iter(hashes)), int)}"


def interning_not_asserted_demo() -> tuple[bool, str]:
    # Do not assert interning; use == not is for value comparison.
    a = "".join(["hello", "world"])  # may or may not be interned
    b = "".join(["hello", "world"])
    equal = a == b
    # Not asserting a is b.
    return equal, "interning-not-asserted"


def mutability_demo() -> tuple[str, str]:
    # Mutable container unhashable; immutable hashable.
    mutable = {"a": 1}
    immutable = (1, 2)
    try:
        hash(mutable)  # type: ignore[arg-type]
        mutable_hash = "hashable"
    except TypeError:
        mutable_hash = "unhashable"
    try:
        hash(immutable)
        immutable_hash = "hashable"
    except TypeError:
        immutable_hash = "unhashable"
    return mutable_hash, immutable_hash


class HashableRecord:
    def __init__(self, name: str, value: int) -> None:
        self.name = name
        self.value = value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, HashableRecord):
            return (self.name, self.value) == (other.name, other.value)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.name, self.value))
