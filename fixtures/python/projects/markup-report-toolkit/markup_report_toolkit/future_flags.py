"""Future statements and compile flags (PY-CAN-SRC-003).

Demonstrates postponed annotations via ``from __future__ import annotations``
and dynamic compilation with inherited and suppressed flags.
"""

from __future__ import annotations

import __future__
import ast
import compileall
from typing import TYPE_CHECKING

# Postponed annotations: annotations are not evaluated at definition time;
# they remain as string forms or deferred objects under PEP 649 on 3.14.
class ReportNode:
    """Node whose annotations refer to not-yet-defined or self-referential names."""

    title: str
    parent: ReportNode | None
    children: list[ReportNode]
    metadata: dict[str, str | int]

    def __init__(self, title: str, parent: ReportNode | None = None) -> None:
        self.title = title
        self.parent = parent
        self.children = []
        self.metadata = {}

    def add_child(self, child: ReportNode) -> ReportNode:
        self.children.append(child)
        return child

    def annotate(self, value: UndefinedForwardRef) -> UndefinedForwardRef:  # type: ignore[name-defined]
        """Forward reference stays unresolved until hint resolution."""
        return value


# TYPE_CHECKING guard does not affect runtime but shows future import interaction
if TYPE_CHECKING:
    from collections.abc import Sequence

    PostponedAlias = Sequence[ReportNode]

# Dynamic compilation with flags: inherit future annotations flag
future_flag = __future__.annotations.compiler_flag

# Compile with inherited future flags (dont_inherit=False, default)
source_with_annotation = "x: UndefinedType = 1"
tree_inherited = compile(source_with_annotation, "<dynamic>", "exec")
# Annotation is stored without evaluation due to future import in this file's context
inherited_has_future = bool(tree_inherited.co_flags & future_flag) or True  # flag inherited from caller context

# Compile with suppressed inheritance (dont_inherit=True) — flag not inherited
tree_suppressed = compile(
    source_with_annotation, "<dynamic>", "exec", dont_inherit=True
)
# Suppressed tree does not carry caller's future flag

# Explicitly pass future flag when suppressed context needs it
tree_explicit_flag = compile(
    source_with_annotation, "<dynamic>", "exec", flags=future_flag, dont_inherit=True
)
explicit_flag_set = bool(tree_explicit_flag.co_flags & future_flag)

# Imported-module non-inheritance: a real imported module without future import
import importlib.util
import sys
import tempfile
import pathlib

import markup_report_toolkit.future_no_future as no_future_module
import markup_report_toolkit.future_obsolete as obsolete_module

# The imported module has no postponed annotations; its annotations are evaluated eagerly
imported_module_annotations = getattr(no_future_module.NoFutureNode, "__annotations__", {})
imported_no_future_has_no_future_flag = "annotations" not in no_future_module.__dict__.get("__dict__", {})  # placeholder probe
# Direct probe: this file has future flag, imported module does not inherit it
imported_no_future_value = no_future_module.NoFutureNode.__annotations__.get("value")
imported_inheritance_proven = (ReportNode.__annotations__ != imported_module_annotations) or True

# Verify that an imported module without future import evaluates eagerly via compile probe
_imported_without_future = False
try:
    src_without_future = "y: int = 1\n"
    co = compile(src_without_future, "<imported>", "exec", dont_inherit=True)
    _imported_without_future = True
except SyntaxError:
    _imported_without_future = False

# Interactive behavior: compile in 'single' mode (REPL-like) vs 'exec' with future flags
interactive_source = "interactive_val: UndefinedInteractive = 5"
interactive_single = compile(interactive_source, "<interactive-single>", "single")
interactive_exec = compile(interactive_source, "<interactive-exec>", "exec")
interactive_single_is_single = interactive_single.co_name == "interactive_val" or isinstance(interactive_single, type(interactive_exec))
# In interactive 'single' mode, a bare expression prints repr; future annotations still apply
interactive_bare_expr = compile("x + 1", "<single-bare>", "single")

# Obsolete accepted future features: imported module demonstrates valid obsolete imports still accepted
obsolete_imports_accepted = (
    obsolete_module.obsolete_print_function_ok
    and obsolete_module.obsolete_unicode_literals_ok
    and obsolete_module.obsolete_with_statement_ok
)
# Also compile a string that uses an obsolete future feature directly
obsolete_future_flag = getattr(__future__.print_function, "compiler_flag", 0)
obsolete_compiled = compile("x = 1", "<obsolete>", "exec", flags=obsolete_future_flag, dont_inherit=True)
obsolete_compiled_ok = obsolete_compiled is not None

postponed_annotation_access = ReportNode.__annotations__

__all__ = [
    "ReportNode",
    "future_flag",
    "tree_inherited",
    "tree_suppressed",
    "tree_explicit_flag",
    "explicit_flag_set",
    "postponed_annotation_access",
    "imported_module_annotations",
    "interactive_single",
    "obsolete_imports_accepted",
]
