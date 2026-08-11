"""Built-in generic aliases and unions (PY-CAN-TYPE-003)."""

from __future__ import annotations

import pickle
from typing import Optional

# --- Modern built-in generic aliases ----------------------------------------

def modern_aliases(
    items: list[str],
    mapping: dict[str, int],
    combo: tuple[int, str, float],
    unique: set[str],
    frozen: frozenset[int],
) -> dict[str, list[int]]:
    result: dict[str, list[int]] = {}
    for item in items:
        result[item] = [mapping.get(item, 0)]
    return result


# --- Legacy typing aliases (pre-PEP 585 contrast) ----------------------------

from typing import Dict, List, Tuple, Set, FrozenSet

def legacy_aliases(
    items: List[str],
    mapping: Dict[str, int],
) -> Dict[str, List[int]]:
    return {k: [v] for k, v in mapping.items() if k in items}


# --- Union spellings: modern X|Y vs Optional vs typing.Union -----------------

from typing import Union

def modern_union(value: int | str | None) -> str:
    if isinstance(value, int):
        return str(value)
    if value is None:
        return "none"
    return value


def optional_union(value: Optional[str]) -> str:
    return value if value is not None else ""


def legacy_union(value: Union[int, str]) -> str:
    if isinstance(value, int):
        return f"int:{value}"
    return f"str:{value}"


# --- Introspect origins and arguments ----------------------------------------

def introspect_origins() -> dict[str, object]:
    alias = list[str]
    return {
        "origin": getattr(alias, "__origin__", None) or getattr(alias, "__origin__", None),
        "args": getattr(alias, "__args__", None),
        "modern_list_origin": getattr(list[int], "__origin__", None),
        "typing_list_origin": getattr(List[int], "__origin__", None),
    }


def get_args_demo() -> tuple[object, ...]:
    from typing import get_origin, get_args
    alias = dict[str, int]
    return get_origin(alias), get_args(alias)  # type: ignore[return]


# --- Permitted runtime checks -------------------------------------------------

def permitted_runtime_checks(value: object) -> dict[str, bool]:
    return {
        "is_list": isinstance(value, list),
        "is_dict": isinstance(value, dict),
        "is_instance_of_list_generic": isinstance([], list),
    }


def parameterized_isinstance_failure_demo() -> str:
    """Parameterized ``isinstance`` with subscripted alias fails at runtime."""
    try:
        isinstance([], list[str])  # type: ignore[arg-type]
        return "no-error"
    except TypeError as exc:
        return f"TypeError:{exc}"


# --- Custom metaclass __or__ variant ----------------------------------------

class OrMeta(type):
    def __or__(self, other: object) -> str:
        other_name = getattr(other, "__name__", str(other))
        return f"custom-union:{self.__name__}|{other_name}"

    def __ror__(self, other: object) -> str:
        self_name = getattr(self, "__name__", str(self))
        other_name = getattr(other, "__name__", str(other))
        return f"custom-union:{other_name}|{self_name}"


class CustomA(metaclass=OrMeta):
    pass


class CustomB(metaclass=OrMeta):
    pass


def metaclass_or_demo() -> tuple[object, object, bool]:
    # Built-in union still works.
    union_type = int | str
    return int | str, union_type, (int | str) == union_type


def custom_metaclass_or_demo() -> tuple[str, str]:
    # Exercises the assigned custom metaclass ``__or__`` edge case.
    return (CustomA | CustomB), (CustomA | int)  # type: ignore[operator]


def alias_equality_and_pickling() -> dict[str, bool]:
    a = list[int]
    b = list[int]
    pickled = pickle.loads(pickle.dumps(a))
    return {
        "equality": a == b,
        "pickle_roundtrip": pickled == a,
        "optional_is_union": Optional[int] == Union[int, None],
    }


# --- Optional union variant ---------------------------------------------------

def optional_is_union_with_none() -> bool:
    from typing import get_args, get_origin
    import types
    opt = Optional[str]
    union = Union[str, None]
    modern = str | None
    return get_args(opt) == get_args(union) and modern == opt
