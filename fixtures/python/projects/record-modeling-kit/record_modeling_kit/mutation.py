"""Runtime mutation and rebinding (PY-CAN-OBJ-012)."""

from __future__ import annotations

from typing import Any


class PatchableService:
    version = 1

    def action(self) -> str:
        return f"v{self.version}"

    def helper(self) -> str:
        return "helper"


# Module-level function for patching demo.
def compute(value: int) -> int:
    return value * 2


def patch_module_function_demo() -> tuple[int, int]:
    # Old alias keeps reference to original function.
    old_alias = compute
    # Patch module global.
    globals()["compute"] = lambda v: v * 10
    after = compute(3)  # type: ignore[assignment]
    old_result = old_alias(3)
    # Restore for idempotence.
    globals()["compute"] = old_alias
    return old_result, after


def class_patch_and_alias_demo() -> tuple[str, str]:
    svc = PatchableService()
    bound_before = svc.action  # bound method captures function at access time
    PatchableService.version = 2
    via_lookup = svc.action()
    via_old_bound = bound_before()
    return via_old_bound, via_lookup  # both see new version? bound_before reads self.version live


def qualified_vs_alias_demo() -> tuple[str, str]:
    import record_modeling_kit.mutation as mut

    alias = mut.compute
    # Patch qualified name.
    mut.compute = lambda v: v + 100  # type: ignore[assignment]
    via_alias = alias(1)
    via_qualified = mut.compute(1)
    # Restore.
    mut.compute = alias
    return str(via_alias), str(via_qualified)


def immutable_type_patch_demo() -> str:
    try:
        list.append = lambda self, x: None  # type: ignore[method-assign, assignment]
        return "no-error"
    except (TypeError, AttributeError) as exc:
        return f"immutable-patch:{type(exc).__name__}:{exc}"


def late_descriptor_missing_set_name_demo() -> str:
    class Host:
        pass

    class LateDesc:
        def __set_name__(self, owner: type, name: str) -> None:
            self.name = name  # type: ignore[attr-defined]

        def __get__(self, instance: object | None, owner: type | None = None) -> Any:
            if instance is None:
                return self
            return f"late:{getattr(self, 'name', 'no-name')}"

    d = LateDesc()
    Host.late = d  # type: ignore[attr-defined]
    missing = not hasattr(d, "name")
    host = Host()
    before = host.late  # type: ignore[attr-defined]
    # Manual __set_name__ would fix.
    if missing:
        d.__set_name__(Host, "late")
        after = host.late  # type: ignore[attr-defined]
        return f"before={before} after={after}"
    return before  # type: ignore[return-value]


def deletion_demo() -> str:
    class Temp:
        keep = "keep"
        remove = "remove"

    obj = Temp()
    del Temp.remove
    has_keep = hasattr(Temp, "keep")
    has_remove = hasattr(Temp, "remove")
    return f"keep={has_keep} remove={has_remove}"


def patch_timing_demo() -> tuple[str, str]:
    # Import-time alias vs late lookup.
    from record_modeling_kit.mutation import PatchableService as PS

    svc = PS()
    before = svc.helper()
    PS.helper = lambda self: "patched"  # type: ignore[method-assign, assignment]
    after = svc.helper()
    # Restore.
    PS.helper = lambda self: "helper"  # type: ignore[method-assign, assignment]
    return before, after
