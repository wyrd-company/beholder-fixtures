"""Enumerations (PY-CAN-OBJ-014)."""

from __future__ import annotations

import enum
from enum import Enum, Flag, IntEnum, IntFlag, StrEnum, auto, unique


class Color(Enum):
    RED = 1
    CRIMSON = 1  # alias to RED
    GREEN = 2
    BLUE = 3
    AUTO_BLUE = auto()

    def is_primary(self) -> bool:
        return self in (Color.RED, Color.BLUE, Color.GREEN)


class Status(StrEnum):
    PENDING = auto()
    RUNNING = auto()
    DONE = auto()


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Perm(Flag):
    READ = auto()
    WRITE = auto()
    EXEC = auto()
    ALL = READ | WRITE | EXEC


class Feature(IntFlag):
    A = auto()
    B = auto()
    C = auto()


def alias_demo() -> tuple[str, bool, int]:
    # CRIMSON is alias to RED, omitted from iteration count vs members.
    is_alias = Color.CRIMSON is Color.RED
    members = [m.name for m in Color]
    alias_in_members = "CRIMSON" in [m.name for m in Color.__members__.values()]
    # Alias appears in __members__ but iteration omits duplicates? Actually Color.__members__ includes alias.
    return members[0], is_alias, len(members)


def auto_values_demo() -> tuple[str, str]:
    return Status.PENDING.value, Priority.HIGH.name


def int_string_flag_mixing_demo() -> tuple[bool, bool, bool]:
    # IntEnum mixes with int, StrEnum with str, Flag mixing via bitwise.
    int_compare = Priority.HIGH == 3
    str_compare = Status.DONE == "done" or Status.DONE.value == "done"
    perm = Perm.READ | Perm.WRITE
    has_read = bool(perm & Perm.READ)
    return int_compare, str_compare, has_read


def custom_methods_demo() -> bool:
    return Color.RED.is_primary()


def identity_demo() -> bool:
    # Enum members are singletons.
    return Color.RED is Color.__members__["RED"]


def iteration_demo() -> list[str]:
    return [m.name for m in Perm if m.name is not None]


def value_lookup_demo() -> Color:
    return Color(2)  # lookup by value


def alias_omission_demo() -> tuple[int, int]:
    # Iteration length vs __members__ length shows alias omission.
    iter_len = len(list(Color))
    members_len = len(Color.__members__)
    return iter_len, members_len


def uniqueness_rejection_demo() -> str:
    try:
        @unique
        class Bad(Enum):
            A = 1
            B = 1

        _ = Bad
        return "no-error"
    except ValueError as exc:
        return f"unique-error:{exc}"


def forbidden_member_extension_demo() -> str:
    # Forbidden: subclassing a member-bearing Enum with a new member is rejected.
    try:
        class ExtendedColor(Color):  # type: ignore[misc]
            NEW = 99  # type: ignore[assignment]

        _ = ExtendedColor
        return "no-error"
    except TypeError as exc:
        return f"forbidden-extension:{exc}"


def int_comparison_type_loss_demo() -> tuple[bool, bool, int, type]:
    # IntEnum comparison and arithmetic that loses enum type.
    plain_is_int = isinstance(Color.RED, int)
    intenum_is_int = isinstance(Priority.LOW, int)
    # Operation result loses IntEnum type and becomes plain int.
    result = Priority.HIGH + 1
    is_plain_int = type(result) is int
    return plain_is_int, intenum_is_int, result, type(result).__name__  # type: ignore[return-value]
