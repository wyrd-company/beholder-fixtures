"""Assignment targets and unpacking (PY-CAN-SRC-008).

Covers nested, starred, and chained assignment, attribute and item targets,
overlaps, augmented assignment, and evaluation ordering.
"""

# Basic assignment
simple_assign = 1
chained_assignment = None
a = b = c = 0
chained_assignment = (a, b, c)  # (0, 0, 0)

# Nested unpacking
(nested_a, (nested_b, nested_c)) = (1, (2, 3))
[nested_list_a, nested_list_b] = [10, 20]

# Starred unpacking — result is list
first, *middle, last = [1, 2, 3, 4, 5]
starred_simple = (first, middle, last)  # (1, [2, 3, 4], 5)
*a_star, trailing = [1, 2, 3]
leading, *b_star = [1, 2, 3]

# Chained assignment
x = y = z = []
# Chained assignment shares same object initially; reassignment splits
x = [1]
y = [1]
z = [1]

# Attribute assignment
class ReportSection:
    def __init__(self) -> None:
        self.title = ""
        self.count = 0

section = ReportSection()
section.title = "introduction"
section.count = 5

# Item assignment
data: dict[str, int] = {}
data["key"] = 42
data["other"] = 99
lst = [0, 0, 0]
lst[1] = 10

# Overlapping assignment (swap)
p, q = 1, 2
p, q = q, p  # overlap-safe swap

# Right side evaluated first; target writes in order
eval_order_log: list[str] = []

def _val(v: int, label: str) -> int:
    eval_order_log.append(label)
    return v

eval_order_log.clear()
# Right side computes before any target write
x, y = _val(10, "rhs1"), _val(20, "rhs2")
assignment_right_first = list(eval_order_log)  # ["rhs1", "rhs2"]

# Target evaluated once for augmented assignment
class CountingTarget:
    def __init__(self) -> None:
        self.value = 10
        self.get_count = 0

    def __getitem__(self, key: str) -> int:
        self.get_count += 1
        return self.value

    def __setitem__(self, key: str, val: int) -> None:
        self.value = val

# Augmented assignment: target evaluated once
counter_map = CountingTarget()
# This would evaluate counter_map["k"] once for read, then once for write internally;
# but for attribute, the object is evaluated once.
class AugContainer:
    def __init__(self) -> None:
        self.x = 5

aug = AugContainer()
aug.x += 10  # aug.x = 15, aug evaluated once
aug.x -= 3
aug.x *= 2
aug.x //= 3
aug.x **= 2
aug.x %= 10
aug.x &= 0b111
aug.x |= 0b001
aug.x ^= 0b010
aug.x >>= 1
aug.x <<= 1

# Chained assignment with unpacking
m, n = o, p2 = (100, 200)

# Starred result list
head, *tail = range(5)
tail_is_list = isinstance(tail, list)

# Attribute/item overlap
class Overlap:
    attr = 0

ov = Overlap()
ov.attr, lst[0] = 99, 88

# Arity failures: valid unpacking source that raises ValueError at runtime (not invalid syntax)
try:
    a_arity, b_arity = [1, 2, 3]  # type: ignore[misc]
    arity_too_many = False
except ValueError:
    arity_too_many = True

try:
    x1, y1, z1 = [1, 2]  # type: ignore[misc]
    arity_too_few = False
except ValueError:
    arity_too_few = True

try:
    a2, (b2, c2) = [1, [2]]  # type: ignore[misc]
    nested_arity_fails = False
except ValueError:
    nested_arity_fails = True

# Valid starred handles variable length: correctly matched cases above.

# Assignment versus pattern contrast: unpacking assignment vs match-case pattern
def assignment_vs_pattern(items: list[int]) -> dict[str, object]:
    # Assignment unpacking binds unconditionally (or raises)
    assigned_a, assigned_b = items[:2] if len(items) >= 2 else (None, None)
    # Pattern matching binds only on successful match; uses different syntax
    match items:
        case [p, q]:
            pattern_p, pattern_q = p, q
            pattern_matched = True
        case [p]:
            pattern_p, pattern_q = p, None
            pattern_matched = True
        case _:
            pattern_p, pattern_q = None, None
            pattern_matched = False
    return {
        "assigned": (assigned_a, assigned_b),
        "pattern": (pattern_p, pattern_q),
        "pattern_matched": pattern_matched,
    }

assignment_pattern_contrast = assignment_vs_pattern([10, 20])

__all__ = [
    "nested_a",
    "starred_simple",
    "section",
    "assignment_right_first",
    "tail_is_list",
    "aug",
]
