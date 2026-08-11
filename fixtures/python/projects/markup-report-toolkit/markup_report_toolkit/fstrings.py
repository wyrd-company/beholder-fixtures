"""Formatted string literals (PY-CAN-SRC-005).

Covers conversions, nested format specs, debug ``=``, escaped braces,
multiline and nested expressions, and custom formatting under the 3.12+
f-string grammar. Malformed and pre-3.12 rejected forms are excluded.
"""

import math

name = "report"
count = 42
value = 3.14159
items = ["alpha", "beta", "gamma"]

# Conversions: !s, !r, !a
conversion_s = f"{name!s}"
conversion_r = f"{name!r}"
conversion_a = f"{name!a}"
conversion_on_expression = f"{count!r}"

# Nested format specs
width = 10
precision = 2
nested_format_spec = f"{value:{width}.{precision}f}"
dynamic_spec = f"{value:{width}}"
nested_expression_spec = f"{value:{width + 2}.{precision + 1}f}"

# Debug ``=`` — prints expression text and value
debug_simple = f"{count=}"
debug_with_format = f"{value=:.2f}"
debug_with_conversion = f"{name=!r}"

# Escaped braces — ``{{`` and ``}}`` become single braces
escaped_braces = f"{{literal}} {count} {{}}"
escaped_mixed = f"{{{{nested}}}} {name!r}"

# Multiline f-strings (3.12+ allows multiline expressions inside)
multiline_fstring = f"""Report: {name}
Count: {count}
Value: {value:.2f}
"""
multiline_expression = f"{name.upper()} — {count * 2}"

# Nested expressions — f-string inside f-string
inner = f"{name}"
nested_fstring = f"outer {f'inner {inner}'} end"
nested_with_format = f"result {f'{value:.1f}'}"

# Expressions containing quotes and backslashes (PEP 701: now valid)
quotes_inside = f"{'single'} {'double'}"
backslash_inside = f"{'a\\nb'.encode('unicode_escape').decode()}"
quote_nesting = f'He said {"hello"} and {name!r}'

# Runtime effects inside f-string expression
def _side_effect(x: int) -> int:
    return x * 2

runtime_effect_fstring = f"doubled { _side_effect(count)}"

# Custom formatting via __format__
class MarkupSpan:
    def __init__(self, text: str, style: str = "plain") -> None:
        self.text = text
        self.style = style

    def __format__(self, spec: str) -> str:
        if spec == "upper":
            return self.text.upper()
        if spec == "bold":
            return f"**{self.text}**"
        if spec == "italic":
            return f"*{self.text}*"
        if spec == "":
            return self.text
        return f"{self.text}:{spec}"

custom_plain = f"{MarkupSpan('hello')}"
custom_upper = f"{MarkupSpan('hello'):upper}"
custom_bold = f"{MarkupSpan('hello'):bold}"
custom_nested_spec = f"{MarkupSpan('hello'):{'upper'}}"

# Format spec with conversion interplay
mixed_conversion_format = f"{value!r:{width}}"

# Parser nesting limits: deeply nested f-strings remain valid under 3.12+
deep_nesting = f"{f'{name}'}"

# Concise report template using several features
def render_report(title: str, total: int) -> str:
    span = MarkupSpan(title)
    return (
        f"Report {title!r} "
        f"({total=}) "
        f"formatted {span:upper} "
        f"{{escaped}} "
        f"{value:{width}.{precision}f}"
    )

__all__ = [
    "conversion_s",
    "nested_format_spec",
    "debug_simple",
    "escaped_braces",
    "multiline_fstring",
    "nested_fstring",
    "custom_upper",
    "render_report",
]
