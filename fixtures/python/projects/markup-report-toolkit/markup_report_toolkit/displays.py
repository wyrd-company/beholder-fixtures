"""Collection displays and unpacking (PY-CAN-SRC-007).

Exercises list, set, and dict displays, starred elements, mapping merges,
duplicate keys, and side-effect ordering.
"""

from typing import Any

# Basic displays
list_display = [1, 2, 3]
set_display = {1, 2, 3}
dict_display = {"title": "report", "count": 3}
empty_list = []
empty_set = set()  # {} is dict, not set
empty_dict: dict[str, int] = {}

# Starred elements in list/set/tuple displays
xs = [1, 2]
starred_list = [0, *xs, 3, 4]
starred_set = {0, *xs, 5}
starred_tuple = (0, *xs, 6)

# Nested starred
nested_starred = [*xs, *([3, 4])]

# Mapping merges (PEP 448) — dict unpacking with **
base = {"a": 1, "b": 2}
overlay = {"b": 20, "c": 3}
merged_dict = {**base, **overlay}  # later value for 'b' wins: 20
merged_with_literal = {"x": 0, **base, "y": 99}
duplicate_key_literal = {"key": 1, "key": 2}  # later wins: 2
later_wins = duplicate_key_literal["key"] == 2

# Dict merging vs call duplicate distinction:
# dict literal allows duplicate keys (later wins), call would fail at runtime for duplicate kw
def _consume(a: int, b: int) -> int:
    return a + b

call_kwargs = {"a": 1, "b": 2}
# Call with ** merging — duplicate would raise TypeError at runtime, not syntax
merged_kwargs_call = {**{"a": 1}, **{"b": 2}}

# Duplicate-call: valid call source that raises TypeError at runtime (multiple values for same keyword)
def _expect_two(a: int, b: int) -> int:
    return a + b

try:
    _expect_two(a=1, **{"a": 2})  # type: ignore[arg-type]
    duplicate_call_raises = False
except TypeError:
    duplicate_call_raises = True

try:
    dict(a=1, **{"a": 2})  # type: ignore[arg-type]
    duplicate_call_dict_raises = False
except TypeError:
    duplicate_call_dict_raises = True

# Unhashable key: valid display source that raises TypeError at runtime
try:
    unhashable_display = {[1, 2]: "bad"}  # type: ignore[dict-item]
    unhashable_key_raises = False
except TypeError:
    unhashable_display = {}
    unhashable_key_raises = True

try:
    _tmp: dict[Any, Any] = {}
    _tmp[[1, 2]] = 1  # type: ignore[index]
    unhashable_item_raises = False
except TypeError:
    unhashable_item_raises = True
else:
    unhashable_item_raises = False

# Keep valid hashable keys above; unhashable cases are guarded runtime failures.

# Set order is unspecified — demonstrate that display order is source order but set iteration not guaranteed sorted
set_insertion_order = {3, 1, 2}

# Comprehension key-before-value nuance: dict comprehension value may reference key
dict_comprehension = {k: k * 2 for k in [1, 2, 3]}

# Key-before-value evaluation order in dict comprehension: key side effect before value per iteration
_dict_comp_log: list[str] = []

def _kc(v: int) -> int:
    _dict_comp_log.append(f"k:{v}")
    return v

def _vc(v: int) -> int:
    _dict_comp_log.append(f"v:{v}")
    return v * 10

_dict_comp_log.clear()
dict_comp_key_before_value = {_kc(k): _vc(k) for k in [1, 2]}
key_before_value_order = list(_dict_comp_log)  # ["k:1","v:1","k:2","v:2"] key before value

# Side-effect order — left-to-right evaluation of display elements
_side_effect_log: list[str] = []

def _log(value: int, label: str) -> int:
    _side_effect_log.append(label)
    return value

# Reset and evaluate
_side_effect_log.clear()
ordered_list = [_log(1, "a"), _log(2, "b"), _log(3, "c")]
list_side_effect_order = list(_side_effect_log)  # ["a", "b", "c"]

_side_effect_log.clear()
ordered_dict = {"a": _log(10, "x"), "b": _log(20, "y")}
dict_side_effect_order = list(_side_effect_log)  # ["x", "y"] — value order left-to-right

_side_effect_log.clear()
merged_with_side_effects = {**{"a": _log(1, "m1")}, **{"b": _log(2, "m2")}}
merge_side_effect_order = list(_side_effect_log)  # ["m1", "m2"]

# List comprehension display interaction
list_comp_display = [x * 2 for x in [1, 2, 3]]
set_comp_display = {x * 2 for x in [1, 2, 3]}

# Unpacking in assignment context is covered in assignment.py; here just display forms

__all__ = [
    "list_display",
    "set_display",
    "dict_display",
    "starred_list",
    "merged_dict",
    "duplicate_key_literal",
    "later_wins",
    "ordered_list",
    "list_side_effect_order",
]
