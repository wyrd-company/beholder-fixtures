"""Lines and indentation (PY-CAN-SRC-002).

Exercises nested suites, implicit and explicit line joining, comments,
blank lines, and whitespace handling including form-feed.
"""

# Blank lines and comments are valid and do not affect execution.

# Nested suites: function containing loop containing conditional
def build_report(sections: list[str]) -> list[str]:
    """Build report lines using nested suites."""
    lines: list[str] = []
    for section in sections:
        if section:
            lines.append(f"# {section}")
            for idx, char in enumerate(section):
                if idx % 2 == 0:
                    lines.append(f"  - {char}")
                else:
                    lines.append(f"    * {char}")
        else:
            lines.append("(empty)")
    return lines


# Implicit line joining: inside parentheses, brackets, and braces
implicit_joined = (
    "first"
    + " second"
    + " third"
)

implicit_list = [
    1,
    2,
    3,
]

implicit_dict = {
    "title": "report",
    "author": "toolkit",
}

implicit_call = build_report(
    [
        "intro",
        "body",
        "conclusion",
    ]
)

# Multi-line implicit joining with comments interleaved
implicit_with_comments = [
    1,  # first item
    2,  # second item
    # blank comment line above contributes nothing
    3,
]

# Explicit line joining with backslash
explicit_joined = "alpha " + \
    "beta " + \
    "gamma"

explicit_with_indent = 1 + \
    2 + \
    3

# Form-feed as whitespace (U+000C) — valid between tokens
formfeed_example = "before" + "\f" + "after"  # literal form-feed inside string (contrast)
# Actual form-feed character as whitespace: U+000C between + and 20
formfeed_ws = 10 + 20
formfeed_ws_value = formfeed_ws  # 30, proves form-feed counted as whitespace
# Mixed form-feed and newline implicit joining
formfeed_implicit = [
    1,
    2,
    3,
]

# Comments and blank lines as separate valid lines

# This is a comment line


# Inline comment after code
inline_commented = 42  # trailing comment describes the value

# Blank line above and below are valid

# Explicit joining cannot have trailing comment after backslash —
# that would be invalid and is excluded. Valid backslash must be last
# non-whitespace char on line, so we keep valid form only.

# Mixed nesting depth
def nested_suites_example(n: int) -> int:
    if n > 0:
        for i in range(n):
            while i > 0:
                if i % 2 == 0:
                    i -= 1
                else:
                    break
            else:
                continue
        else:
            return n
    else:
        return 0
    return -1


# Indentation with spaces only (consistent dedent)
# Tab vs space ambiguity is excluded as invalid; we use spaces exclusively.
__all__ = [
    "build_report",
    "implicit_joined",
    "implicit_list",
    "implicit_dict",
    "implicit_call",
    "explicit_joined",
    "nested_suites_example",
]
