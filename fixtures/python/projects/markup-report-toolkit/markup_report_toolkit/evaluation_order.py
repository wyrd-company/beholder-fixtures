"""Expression evaluation order (PY-CAN-SRC-010).

Records left-to-right evaluation across arithmetic, calls, displays,
chained comparisons, conditional expressions, and assignment targets.
Precedence is separate from evaluation order; optimizer preserves side effects.
"""

# Left-to-right evaluation logger
_eval_log: list[str] = []

def _logged(value: int, label: str) -> int:
    _eval_log.append(label)
    return value

def _clear_log() -> None:
    _eval_log.clear()

# Arithmetic — operands evaluated left-to-right despite precedence
_clear_log()
arith_result = _logged(2, "a") + _logged(3, "b") * _logged(4, "c")
arith_order = list(_eval_log)  # ["a", "b", "c"]

_clear_log()
arith_with_parens = (_logged(2, "a2") + _logged(3, "b2")) * _logged(4, "c2")
arith_parens_order = list(_eval_log)

# Calls — function and arguments left-to-right
def _add(x: int, y: int) -> int:
    return x + y

_clear_log()
call_result = _add(_logged(10, "arg1"), _logged(20, "arg2"))
call_order = list(_eval_log)  # ["arg1", "arg2"]

_clear_log()
nested_call = _add(_logged(1, "outer1"), _add(_logged(2, "inner1"), _logged(3, "inner2")))
nested_call_order = list(_eval_log)  # ["outer1", "inner1", "inner2"] — inner call args after outer first arg

# Displays — elements evaluated left-to-right
_clear_log()
display_list = [_logged(1, "d1"), _logged(2, "d2"), _logged(3, "d3")]
display_list_order = list(_eval_log)

_clear_log()
display_dict = {"a": _logged(1, "da"), "b": _logged(2, "db")}
display_dict_order = list(_eval_log)  # ["da", "db"]

_clear_log()
display_tuple = (_logged(5, "t1"), _logged(6, "t2"))
display_tuple_order = list(_eval_log)

# Chained comparisons — middle operand evaluated once
_chain_eval_count = 0

def _chain_val(v: int, label: str) -> int:
    global _chain_eval_count
    _chain_eval_count += 1
    _eval_log.append(label)
    return v

_clear_log()
_chain_eval_count = 0
# chained: a < b < c ; b evaluated once
chained = _chain_val(1, "ca") < _chain_val(2, "cb") < _chain_val(3, "cc")
chained_order = list(_eval_log)  # ["ca", "cb", "cc"] with each once
chained_counts = _chain_eval_count  # 3

# Exception stops later operands
_clear_log()

def _raise_after(label: str) -> int:
    _eval_log.append(label)
    raise ValueError(label)

_eval_log.clear()
exception_stops = False
try:
    _ = _logged(1, "e1") + _raise_after("e2") + _logged(3, "e3")
except ValueError:
    exception_stops = True
# e3 never logged because exception stops evaluation
exception_order = list(_eval_log)  # ["e1", "e2"]

# Conditional expression — only chosen branch evaluated
_clear_log()
cond = True
conditional_result = _logged(100, "chosen") if cond else _logged(200, "unchosen")
conditional_order = list(_eval_log)  # ["chosen"]

_clear_log()
cond = False
conditional_result2 = _logged(100, "chosen2") if cond else _logged(200, "unchosen2")
conditional_order2 = list(_eval_log)  # ["unchosen2"]

# Assignment target — target expression evaluated once
_clear_log()

class _Container:
    def __init__(self) -> None:
        self.items: list[int] = [0, 0, 0]

    def __getitem__(self, idx: int) -> int:
        _eval_log.append(f"get:{idx}")
        return self.items[idx]

    def __setitem__(self, idx: int, value: int) -> None:
        _eval_log.append(f"set:{idx}")
        self.items[idx] = value

container = _Container()
_clear_log()

def _index(label: str) -> int:
    _eval_log.append(label)
    return 1

# Target evaluated once in normal assignment — right side first
container[_index("tgt")] = _logged(99, "val")
target_eval_order = list(_eval_log)  # ["val", "tgt", "set:1"] — right side first, target evaluated once


# Precedence vs order note: * has higher precedence but evaluation still left-to-right
_precedence_vs_order = "precedence determines grouping; evaluation is left-to-right"

__all__ = [
    "arith_order",
    "call_order",
    "display_list_order",
    "chained_order",
    "chained_counts",
    "exception_order",
    "conditional_order",
    "target_eval_order",
]
