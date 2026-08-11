"""Literal, Final, ClassVar, and ReadOnly intent (PY-CAN-TYPE-011)."""

from __future__ import annotations

import dataclasses
from enum import Enum
from typing import ClassVar, Final, Literal, LiteralString, TypedDict, ReadOnly

# --- Literal as discriminant --------------------------------------------------

Mode = Literal["create", "update", "delete"]
StatusCode = Literal[200, 404, 500]


def handle_mode(mode: Mode) -> str:
    if mode == "create":
        return "created"
    if mode == "update":
        return "updated"
    return "deleted"


# Enum literals
class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


ColorLiteral = Literal[Color.RED, Color.GREEN]
ExtendedLiteral = Literal[Color.RED, Color.GREEN, Color.BLUE]


# LiteralString (PEP 675, Python 3.11+)
def literal_string_demo(value: LiteralString) -> LiteralString:
    return value


def takes_literal_string(value: LiteralString) -> str:
    return value.upper()


# --- Final module and class names ---------------------------------------------

MODULE_VERSION: Final = "1.0.0"
FINAL_LIST: Final[list[str]] = ["a", "b"]


class Config:
    MAX_RETRIES: Final[int] = 3
    timeout: Final[int] = 30

    def __init__(self, timeout: int) -> None:
        # Instance Final assigned once in __init__
        self.timeout = timeout


# --- Dataclass ClassVar variant -----------------------------------------------

@dataclasses.dataclass
class Batch:
    label: str
    quantity: int
    kind: ClassVar[str] = "batch"
    counter: ClassVar[int] = 0


@dataclasses.dataclass
class ExtendedBatch(Batch):
    unit: str = "pcs"


# --- Deliberate static violations (valid at runtime) --------------------------

# At runtime ``Final`` and ``Literal`` are not enforced; reassignment succeeds
# but a checker would flag it.
def deliberate_final_violation() -> str:
    global MODULE_VERSION
    MODULE_VERSION = "2.0.0"  # type: ignore[assignment] — static violation, runtime ok
    return MODULE_VERSION  # type: ignore[return]


def deliberate_literal_violation() -> Mode:
    bad: Mode = "invalid"  # type: ignore[assignment] — literal violation at static time
    return bad


# --- Nested qualifier rules variant -------------------------------------------

# ``Final`` inside ``ClassVar`` and vice versa follows typing spec nesting rules.
class NestedQualifiers:
    # Final ClassVar: final class variable
    VERSION: Final[ClassVar[str]] = "1.0"  # type: ignore[type-arg]
    # ClassVar inside dataclass already shown above


# --- ReadOnly TypedDict keys variant -----------------------------------------

class ReadOnlyRecord(TypedDict):
    label: ReadOnly[str]
    count: int


def readonly_typed_dict_demo() -> ReadOnlyRecord:
    record: ReadOnlyRecord = {"label": "widget", "count": 5}
    # Reassignment of a ReadOnly key would be a static violation.
    record["count"] = 10  # non-readonly key: ok
    return record


# --- Little runtime enforcement note -----------------------------------------

def little_runtime_enforcement_demo() -> bool:
    # ``Literal`` and ``Final`` have no runtime enforcement beyond normal assignment.
    x: Literal["a", "b"] = "c"  # type: ignore[assignment]
    y: Final[int] = 1
    y = 2  # type: ignore[assignment]
    return x == "c" and y == 2
