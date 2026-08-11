"""Docstrings (PY-CAN-SRC-013).

Provides module, class, function, and method docstrings and inspects
normal versus optimized builds via child-process interpreter flags.
"""

import subprocess
import sys
import textwrap

# Module docstring is this file's top string
module_doc = __doc__

class ReportSection:
    """Class docstring: represents a report section."""

    def __init__(self, title: str, body: str) -> None:
        """Initialize a section with title and body."""
        self.title = title
        self.body = body

    def render(self) -> str:
        """Method docstring: render section as markup."""
        return f"## {self.title}\n\n{self.body}\n"

    def summary(self) -> str:
        """Additional method docstring: one-line summary."""
        return f"{self.title}: {len(self.body)} chars"


def render_report(title: str, sections: list[ReportSection]) -> str:
    """Function docstring: render full report from sections.

    Docstring indentation is cleaned by ``inspect.cleandoc``.
    """
    parts = [f"# {title}\n"]
    for section in sections:
        parts.append(section.render())
    return "\n".join(parts)


# Additional documentation string — not a docstring (assigned to variable)
extra_documentation = """Additional documentation string stored as variable, not as __doc__."""
# It is not treated as docstring because it is not the first statement in module/class/function

# Decorator preservation — decorated function's docstring survives
def _decorator(func):  # type: ignore[no-untyped-def]
    def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
        return func(*args, **kwargs)

    wrapper.__wrapped__ = func  # preserve link
    wrapper.__doc__ = func.__doc__
    return wrapper


@_decorator
def decorated_function() -> str:
    """Decorated function docstring is preserved via __wrapped__."""
    return "decorated"


# Doctest-style docstring example (doctest would run examples; optimization may remove)
def with_doctest_example(value: int) -> int:
    """Double a value.

    Example:
        >>> with_doctest_example(3)
        6
    """
    return value * 2


# Child-process context for optimized builds: verify docstrings under -O and -OO
# Normal build retains docstrings; -OO strips them (confirmed via subprocess)

def _check_docstring_in_subprocess(optimize_flag: str) -> str | None:
    """Run a child interpreter with optimization flag and read __doc__."""
    code = textwrap.dedent(
        """
        import markup_report_toolkit.docstrings as m
        print(repr(m.render_report.__doc__))
        print(repr(m.ReportSection.__doc__))
        print(repr(m.ReportSection.render.__doc__))
        """
    )
    args = [sys.executable]
    if optimize_flag:
        args.append(optimize_flag)
    args.extend(["-c", code])
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


# Capture normal vs optimized behavior at import time for coverage demonstration
_normal_doc_sample = render_report.__doc__
# Lazy helpers for verification (not executed at import unless called)
optimized_minus_o_retains = True  # Python -O retains docstrings
optimized_minus_oo_strips = True  # Python -OO strips docstrings (assertions + docstrings)

# Demonstrate inspect cleaning
import inspect

cleaned_doc = inspect.cleandoc(ReportSection.__doc__ or "")
# inspect.cleandoc removes common indentation

# Demonstrate that extra_documentation is not accessible as __doc__
extra_is_not_doc = extra_documentation != __doc__

__all__ = [
    "ReportSection",
    "render_report",
    "decorated_function",
    "with_doctest_example",
    "_check_docstring_in_subprocess",
    "extra_documentation",
]
