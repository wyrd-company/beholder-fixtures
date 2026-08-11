"""Type aliases (PY-CAN-TYPE-004)."""

from __future__ import annotations

from typing import TypeAlias

# --- Simple assignment alias --------------------------------------------------

SimpleAlias = int
StringList = list[str]

# --- TypeAlias-qualified alias -----------------------------------------------

ExplicitAlias: TypeAlias = dict[str, int]
AnotherAlias: TypeAlias = StringList | None


# --- Recursive alias (self-referential structure) -----------------------------

# Recursive type alias via stringized forward reference.
JsonValue: TypeAlias = str | int | float | bool | None | list["JsonValue"] | dict[str, "JsonValue"]


# --- Generic alias ------------------------------------------------------------

from typing import TypeVar

T = TypeVar("T")

GenericAlias: TypeAlias = list[T]
PairAlias: TypeAlias = tuple[T, T]


# --- 3.12 ``type`` statement --------------------------------------------------

type InventoryId = int
type Box[T] = list[T]
type MappingAlias[K, V] = dict[K, V]
type RecursiveNode = dict[str, "RecursiveNode"] | list["RecursiveNode"] | str


# --- Alias is not a class ----------------------------------------------------

def alias_is_not_class_demo() -> dict[str, bool]:
    return {
        "simple_alias_is_type": isinstance(SimpleAlias, type),  # aliased int
        "type_statement_is_typealiastype": type(InventoryId).__name__ == "TypeAliasType",
        "alias_not_instance": not isinstance(42, SimpleAlias),  # type: ignore[arg-type]
    }


def type_alias_type_demo() -> str:
    # ``type X = ...`` creates a TypeAliasType with lazy evaluation.
    return type(InventoryId).__name__


# --- Lazy TypeAliasType and forward value ------------------------------------

type ForwardAlias = "Batch"
class Batch:
    label: str


def lazy_forward_demo() -> object:
    # ``ForwardAlias`` references ``Batch`` before its definition via lazy eval.
    return ForwardAlias


# --- Parameter scope variant --------------------------------------------------

type ScopedPair[A, B] = tuple[A, B]
type NestedScoped[X] = ScopedPair[X, int]


# --- Pre-3.12 parse failure note ---------------------------------------------

# Before Python 3.12, ``type X = Y`` was a SyntaxError. On 3.14 it parses
# and creates a TypeAliasType; legacy assignment form ``X: TypeAlias = Y``
# remains valid in both eras.

LegacyAlias: TypeAlias = int | str
type ModernAlias = int | str
