"""Assignment expressions (PY-CAN-SRC-009).

Uses walrus operator in loop, condition, parenthesized, and comprehension
positions. Pre-3.8 parse failure excluded; all examples valid on 3.12+.
"""

import io
import re

# Walrus in while loop condition
def read_chunks(buffer: io.StringIO) -> list[str]:
    """Read buffer in chunks using walrus in while condition."""
    chunks: list[str] = []
    data = io.StringIO(buffer.getvalue())
    while chunk := data.read(4):
        chunks.append(chunk)
    return chunks

# Walrus in if condition
def classify_length(items: list[str]) -> str:
    if (n2 := len(items)) > 3:
        return f"long:{n2}"
    else:
        return f"short:{n2}"

def check_threshold(values: list[int], limit: int = 10) -> str:
    if (total := sum(values)) > limit:
        return f"exceeds:{total}"
    return f"within:{total}"

# Walrus in parenthesized expression
parenthesized_walrus = (y := 10) + y  # y=10, result 20
parenthesized_multiple = ((a := 5) + (b := 6)) * (a + b)

# Walrus in comprehension binding — binds in enclosing scope, not comprehension scope
def walrus_in_comprehension(source: list[str]) -> tuple[list[int], int | None]:
    # Capture transformed length that satisfies filter
    filtered = [length for item in source if (length := len(item)) > 3]
    # 'length' remains bound after comprehension in Python 3.8+ where walrus leaks to enclosing scope
    return filtered, length  # type: ignore[name-defined, possibly-undefined]

def walrus_in_comprehension_top(items: list[int]) -> list[int]:
    # Walrus inside comprehension value expression
    return [y for x in items if (y := x * 2) > 4]

# Walrus simple-name-only: target must be a single name, not attribute/item
# Forbidden positions excluded; valid loop/condition/parenthesized/comprehension above are sufficient

# Iteration-variable conflict illustration: walrus shadows loop variable intentionally
def walrus_shadows_loop(items: list[int]) -> int:
    # Walrus binding in condition sees enclosing scope
    result = 0
    for item in items:
        if (result := item * 2) > 5:
            break
    return result

# Walrus in lambda/conditional position also valid
walrus_in_conditional_expr = (val := 42) if (val2 := 10) > 5 else 0  # type: ignore[name-defined]

# Walrus with regex match (common idiom)
def find_markup_tag(text: str) -> str | None:
    pattern = re.compile(r"<(\w+)>")
    if match := pattern.search(text):
        return match.group(1)
    return None

__all__ = [
    "read_chunks",
    "classify_length",
    "check_threshold",
    "parenthesized_walrus",
    "walrus_in_comprehension",
    "find_markup_tag",
]
