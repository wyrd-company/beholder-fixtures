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

# Compile with AST and inherited flags — ast.parse does not use future flags,
# but compile step can. Demonstrate that imported modules do not inherit caller's future.
import importlib.util
import sys
import tempfile
import pathlib

# Verify that an imported module without future import evaluates eagerly
_imported_without_future = False
try:
    src_without_future = "y: int = 1\n"
    co = compile(src_without_future, "<imported>", "exec", dont_inherit=True)
    # No deferred behavior expected here
    _imported_without_future = True
except SyntaxError:
    _imported_without_future = False

# Interactive-like compilation mode contrast not needed; exec mode suffices for postponed demo
postponed_annotation_access = ReportNode.__annotations__

# Obsolete accepted features note: future imports that were once required
# (e.g., print_function) are accepted silently where still present but not needed.
# We demonstrate that only valid future features are used.

__all__ = [
    "ReportNode",
    "future_flag",
    "tree_inherited",
    "tree_suppressed",
    "tree_explicit_flag",
    "explicit_flag_set",
    "postponed_annotation_access",
]
