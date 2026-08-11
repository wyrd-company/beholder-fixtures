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
    """Contrast function `locals()` write-through behavior under PEP 667."""

    layer = "initial"

    def worker() -> dict[str, object]:
        snapshot = dict(locals())
        locals()["layer"] = "mutated"
        return snapshot

    before = worker()
    return {"before": before, "after": layer}


def closure_exec_support(free_value: str) -> str:
    """Execute code that closes over a parameter name."""

    namespace: dict[str, object] = {"free_value": free_value}

    def runner() -> str:
        exec("result = free_value.upper()", namespace)
        return str(namespace["result"])

    return runner()


def untrusted_mapping_guard(user_code: str) -> MappingProxyType:
    """Reject untrusted input by using an isolated, read-only view."""

    sandbox_globals: dict[str, object] = {"__builtins__": {}}
    sandbox_locals: dict[str, object] = {}
    exec(user_code, sandbox_globals, sandbox_locals)
    return MappingProxyType(sandbox_locals)
