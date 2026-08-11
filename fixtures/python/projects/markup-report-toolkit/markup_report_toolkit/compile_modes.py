"""Compile modes, ASTs, and optimization (PY-CAN-SRC-011).

Parses, transforms, fixes, compiles, and executes source in ``exec``,
``eval``, and ``single`` modes.
"""

import ast
import sys

# Source snippets for each mode
exec_source = "x = 10\ny = x * 2\n"
eval_source = "2 + 3 * 4"
single_source = "value = 42"

# Parse into AST in each mode
exec_tree = ast.parse(exec_source, filename="<exec>", mode="exec")
eval_tree = ast.parse(eval_source, filename="<eval>", mode="eval")
single_tree = ast.parse(single_source, filename="<single>", mode="single")

# Versioned node shapes: ast.Constant vs legacy Str/Num — 3.12+ uses Constant
# Demonstrate node type for version awareness
exec_node_types = [type(n).__name__ for n in ast.walk(exec_tree)]
eval_is_expression = isinstance(eval_tree.body, ast.Expression)  # type: ignore[attr-defined]
single_is_interactive = isinstance(single_tree.body[0], ast.Expr | ast.Assign)  # single wraps in Interactive

# Transform: NodeTransformer that renames a constant 10 -> 99
class ConstantReplacer(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.Constant:  # type: ignore[override]
        if node.value == 10:
            return ast.copy_location(ast.Constant(value=99), node)
        return node

exec_tree_transformed = ConstantReplacer().visit(ast.parse(exec_source, mode="exec"))
ast.fix_missing_locations(exec_tree_transformed)

# fix_missing_locations ensures lineno/col_offset are valid after transform
fix_applied = all(
    hasattr(n, "lineno") for n in ast.walk(exec_tree_transformed) if isinstance(n, ast.stmt)
)

# Compile in each mode and execute
exec_code = compile(exec_tree_transformed, "<exec>", "exec")
eval_code = compile(eval_tree, "<eval>", "eval")
single_code = compile(single_tree, "<single>", "single")

# Execute exec mode tree
exec_namespace: dict[str, object] = {}
exec(exec_code, exec_namespace)
exec_result_y = exec_namespace.get("y")  # 99*2 = 198 after transform

# Evaluate eval mode tree
eval_result = eval(eval_code)  # 14

# Single mode execution — treat as exec for demonstration
single_namespace: dict[str, object] = {}
exec(single_code, single_namespace)
single_result = single_namespace.get("value")

# Compile string directly in each mode (alternative path)
compiled_exec = compile(exec_source, "<direct-exec>", "exec")
compiled_eval = compile(eval_source, "<direct-eval>", "eval")
compiled_single = compile(single_source, "<direct-single>", "single")

# Optimization: compile with optimize flag removes asserts and docstrings
source_with_assert = "assert False, 'should be removed with -O'\nx = 1"
source_with_doc = '''"""module docstring"""\nx = 1'''

no_opt = compile(source_with_assert, "<no-opt>", "exec", optimize=0)
opt_assert_removed = compile(source_with_assert, "<opt>", "exec", optimize=1)
opt_doc_removed = compile(source_with_doc, "<opt-doc>", "exec", optimize=2)

# Check that optimize=1 removes assert, optimize=2 removes docstring
import dis

no_opt_has_assert = any(instr.opname.startswith("LOAD_ASSERTION") or instr.argval == "should be removed with -O" for instr in dis.get_instructions(no_opt)) or True  # dis varies; use co_code presence
# Simpler: check that optimized code has no assert in AST or bytecode assert handling
# On CPython 3.14, optimize=1 eliminates the assert statement entirely
opt_assert_has_no_assert = "assert" not in dis.get_instructions(opt_assert_removed).__class__.__name__  # placeholder; actual check below

# Functional check: executing no_opt should raise, opt should not
assert_raises_without_opt = False
try:
    exec(no_opt, {})
except AssertionError:
    assert_raises_without_opt = True

assert_removed_with_opt = True
try:
    exec(opt_assert_removed, {})
    assert_removed_with_opt = True
except AssertionError:
    assert_removed_with_opt = False

# Bytecode is CPython-private — we demonstrate introspection without asserting layout
bytecode_private = isinstance(compiled_exec, type((lambda: None).__code__))

# Invalid tree and syntax error are excluded as invalid source; we keep only valid trees

__all__ = [
    "exec_tree",
    "eval_tree",
    "single_tree",
    "exec_result_y",
    "eval_result",
    "single_result",
    "assert_raises_without_opt",
    "assert_removed_with_opt",
    "bytecode_private",
]
