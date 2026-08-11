"""Soft keywords and grammar version (PY-CAN-SRC-014).

Uses ``match``, ``case``, ``_``, and ``type`` as identifiers where legal
and as syntax where contextual. Requires Python 3.10+ for match/case
and 3.12+ for type statement.
"""

from typing import Any

# Soft keywords as identifiers — legal outside pattern/type contexts
match = "match-as-identifier"
case = "case-as-identifier"
_ = "underscore-as-identifier"
type = "type-as-identifier"  # shadows builtin, legal as variable

# Reassign soft names to prove they are ordinary bindings
match_identifier_value = match
case_identifier_value = case
underscore_identifier_value = _
type_identifier_value = type

# Using soft keywords as attributes and function names is also legal
class CaseContainer:
    def match(self) -> str:  # method named 'match'
        return "method-match"

    def case(self) -> str:
        return "method-case"

    type = "attribute-type"


def _helper(value: Any) -> str:
    return str(value)


# Soft keywords as syntax: match / case pattern matching

def classify_report_node(node: dict[str, Any]) -> str:
    """Classify a report node using match/case syntax."""
    match node:
        case {"kind": "section", "title": title}:
            return f"section:{title}"
        case {"kind": "paragraph", "text": text} if len(text) > 0:
            return f"paragraph:{text[:10]}"
        case {"kind": _, "extra": extra}:  # wildcard _ does not bind
            return f"other:{extra}"
        case _:
            return "unknown"


def match_with_wildcard(value: Any) -> str:
    match value:
        case "alpha":
            return "alpha"
        case _:  # wildcard pattern, _ does not bind
            return "wildcard"


# Demonstrate that wildcard _ in pattern does not create a binding
def wildcard_no_bind_demo(value: Any) -> bool:
    _before = "before"
    match value:
        case _:
            # _ remains "before" if it was defined before, or is not bound here
            pass
    # In this file, _ at module scope is "underscore-as-identifier" — wildcard should not overwrite?
    # Actually module-level _ is shadowed per match case no-bind, but Python's wildcard
    # does not assign to _. Verify:
    return _ == "underscore-as-identifier"

wildcard_preserves = wildcard_no_bind_demo("anything")

# Type as soft keyword: ``type`` statement (Python 3.12+) vs ``type`` identifier
# The ``type`` keyword is soft in type-alias statements.
type ReportTitle = str
type SectionMap = dict[str, str]

# Using ``type`` as identifier after type statement is still legal in assignment context
type_alias_title = ReportTitle  # value is still str
type_alias_map = SectionMap

# Confuse checker by reusing ``type`` as variable after type statement
type_after = "still identifier after type statement"
type_reuse_ok = (type_after == "still identifier after type statement")

# Match/case vs identifier disambiguation across scopes
def soft_keyword_contexts() -> dict[str, str]:
    # Inside function, match/case as syntax vs assignment
    match match:  # first 'match' is syntax, second is identifier value
        case "match-as-identifier":
            result = "matched identifier value via pattern"
        case _:
            result = "no match"
    case = "local-case-identifier"
    return {"result": result, "case": case}


__all__ = [
    "match",
    "case",
    "_",
    "type",
    "classify_report_node",
    "match_with_wildcard",
    "ReportTitle",
    "SectionMap",
    "soft_keyword_contexts",
]
