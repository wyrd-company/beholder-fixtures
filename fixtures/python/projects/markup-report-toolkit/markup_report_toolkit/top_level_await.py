"""Top-level await and interactive compilation (PY-CAN-SRC-012).

Compiles top-level async syntax with ``PyCF_ALLOW_TOP_LEVEL_AWAIT`` and
contrasts ordinary-module rejection.
"""

import ast
import asyncio

# Flag for top-level await compilation
allow_top_level_await = ast.PyCF_ALLOW_TOP_LEVEL_AWAIT

# Top-level await source — valid only with the flag
await_source = "await asyncio.sleep(0)\nexecuted_via_compiled = 42"

# Compile with flag — succeeds as coroutine-like top-level
compiled_with_flag = compile(
    await_source, "<await-top>", "exec", flags=allow_top_level_await
)
# The resulting code object is a coroutine-type when top-level await is allowed
is_coroutine_flag_set = bool(compiled_with_flag.co_flags & 0x80)  # CO_COROUTINE
_has_await = True

# Execute the flagged compiled code object under controlled loop ownership and record result
import types

_compiled_flag_globals: dict[str, object] = {"asyncio": asyncio}
_compiled_flag_coro = types.FunctionType(compiled_with_flag, _compiled_flag_globals)()  # type: ignore[arg-type]
# Verify it is a coroutine and run it
is_top_level_coro = asyncio.iscoroutine(_compiled_flag_coro)
asyncio.run(_compiled_flag_coro)
compiled_top_level_executed_result = _compiled_flag_globals.get("executed_via_compiled")
compiled_top_level_executed_ok = compiled_top_level_executed_result == 42

# Contrast: ordinary module compilation without flag rejects top-level await
ordinary_rejects = False
try:
    compile(await_source, "<await-ordinary>", "exec")
except SyntaxError:
    ordinary_rejects = True

# Also test via ast.parse with feature version and flag
try:
    tree_no_flag = ast.parse(await_source, mode="exec")
    compile(tree_no_flag, "<await-ast-no-flag>", "exec")
    ast_without_flag_rejects = False
except SyntaxError:
    ast_without_flag_rejects = True

# Parse with flag via ast.PyCF_ALLOW_TOP_LEVEL_AWAIT combination
tree_with_flag = ast.parse(await_source, mode="exec")
# ast.parse itself does not apply the flag; compile does — so we demonstrate the compile path

# Executing top-level await requires an async context / event loop
async def _run_top_level() -> str:
    # Equivalent of top-level await execution via async wrapper
    await asyncio.sleep(0)
    return "await-completed"

top_level_result = asyncio.run(_run_top_level())
# Keep separate from compiled execution above; both prove coroutine behavior

# Top-level await is not importable as ordinary module source; it requires
# the flag. Ordinary ``exec(compile(...))`` without flag fails as shown above.
# Async source in function is always valid without flag — contrast
async_source_inside_function = "async def f():\n    await asyncio.sleep(0)\n"
compiled_inside = compile(async_source_inside_function, "<async-def>", "exec")
inside_compiles_without_flag = True  # async def's own await needs no top-level flag

# Interactive single mode with await — flagged single compilation
single_await_source = "await asyncio.sleep(0)"
compiled_single_with_flag = compile(
    single_await_source, "<await-single>", "single", flags=allow_top_level_await
)
single_with_flag_ok = compiled_single_with_flag is not None

__all__ = [
    "compiled_with_flag",
    "ordinary_rejects",
    "top_level_result",
    "inside_compiles_without_flag",
    "single_with_flag_ok",
]
