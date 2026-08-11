"""PKG-009 Requires-Python versus grammar alignment."""

from __future__ import annotations
import sys

# pyproject declares Requires-Python >=3.10 — source uses 3.10+ syntax (match/case).
# Demonstrate accepted vs rejected grammar boundaries via metadata.

REQUIRES_PYTHON = ">=3.10"
SUPPORTED = (3, 10)
GUARDED_DEPENDENCY = "typing-extensions; python_version >= '3.10'"


def uses_modern_syntax(value: object) -> str:
    """Uses match statement (Python 3.10+) — would fail on <3.10."""
    match value:
        case str(s):
            return f"str:{s}"
        case int(n):
            return f"int:{n}"
        case _:
            return "other"


def check_interpreter_boundary() -> dict[str, object]:
    return {
        "requires_python": REQUIRES_PYTHON,
        "current": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "accepted": sys.version_info >= SUPPORTED,
        "grammar": "match/case (3.10+)",
        "alternative_implementation": "PyPy/CPython both support same grammar at this version",
        "universal_tag_note": "py3-none-any wheel tag does not override Requires-Python; installer still checks",
        "sdist_minimum_note": "sdist backend minimum is advisory; installer enforces Requires-Python on install",
    }
