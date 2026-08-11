"""`exec`, `eval`, and explicit namespaces (PY-CAN-BIND-008)."""

from __future__ import annotations

from types import MappingProxyType


def exec_in_mappings(code: str, globals_map: dict[str, object], locals_map: dict[str, object]) -> dict[str, object]:
    """Define and read names in separate global and local mappings."""

    exec(code, globals_map, locals_map)
    return {"globals": dict(globals_map), "locals": dict(locals_map)}


def eval_in_mappings(expression: str, globals_map: dict[str, object], locals_map: dict[str, object]) -> object:
    """Evaluate an expression against explicit namespaces."""

    return eval(expression, globals_map, locals_map)


def function_locals_snapshot() -> dict[str, object]:
    """Contrast optimized-scope `locals()` snapshots and unreliable mapping mutation."""

    def worker() -> dict[str, object]:
        fast_local = "initial"
        first_snapshot = dict(locals())
        live_view = locals()
        try:
            live_view["fast_local"] = "mutated"
            mutation_visible = live_view.get("fast_local")
        except Exception:
            mutation_visible = "failed"
        second_snapshot = dict(locals())
        return {
            "first_snapshot": first_snapshot.get("fast_local"),
            "second_snapshot": second_snapshot.get("fast_local"),
            "mutation_visible": mutation_visible,
            "live_value": fast_local,
        }

    return worker()


def closure_exec_support(free_value: str) -> str:
    """Execute compiled code with a free variable through the `closure` parameter."""

    result_holder: str | None = None

    def make_runner() -> callable:
        captured = free_value

        def runner() -> None:
            nonlocal result_holder
            result_holder = captured.upper()

        return runner

    runner = make_runner()
    exec(runner.__code__, runner.__globals__, closure=runner.__closure__)
    return result_holder or ""


def untrusted_mapping_guard(user_code: str) -> MappingProxyType:
    """Reject untrusted input by using an isolated, read-only view."""

    sandbox_globals: dict[str, object] = {"__builtins__": {}}
    sandbox_locals: dict[str, object] = {}
    exec(user_code, sandbox_globals, sandbox_locals)
    return MappingProxyType(sandbox_locals)
