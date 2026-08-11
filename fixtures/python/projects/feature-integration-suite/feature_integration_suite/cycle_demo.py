"""Circular import introspection demo (PY-CAN-INT-003) - resolve hints with and without namespaces, eager vs stringized."""

from __future__ import annotations

import typing

from feature_integration_suite import cycle_a, cycle_b


def resolve_with_namespace() -> dict[str, object]:
    """Break cycle statically, then resolve hints successfully with namespaces."""
    hints_a = typing.get_type_hints(
        cycle_a.NodeA,
        globalns=vars(cycle_a) | {"NodeB": cycle_b.NodeB, "HelperB": cycle_b.HelperB, "AliasedHelper": cycle_b.HelperB},
        include_extras=True,
    )
    hints_b = typing.get_type_hints(
        cycle_b.NodeB,
        globalns=vars(cycle_b) | {"NodeA": cycle_a.NodeA},
        include_extras=True,
    )
    return {"NodeA_hints_keys": sorted(hints_a.keys()), "NodeB_hints_keys": sorted(hints_b.keys())}


def resolve_without_namespace_failure() -> str:
    """Same hints without supplemental namespace should raise due to missing HelperB alias."""
    try:
        # NodeA.alias_loss_field is "HelperB | None" but HelperB not in NodeA's module globals
        typing.get_type_hints(cycle_a.NodeA, include_extras=True)
        return "no-error"
    except NameError as exc:
        return f"name-error:{exc.__class__.__name__}"
    except Exception as exc:  # noqa: BLE001
        return f"other-error:{exc.__class__.__name__}:{exc}"


def eager_vs_stringized_regime() -> dict[str, object]:
    """On Python 3.14 annotations are deferred (PEP 649); demonstrate stringized storage."""
    ann = cycle_a.NodeA.__annotations__
    # With `from __future__ import annotations`, values are strings
    is_stringized = all(isinstance(v, str) for v in ann.values())
    # Runtime bases / decorators still need real importable object
    runtime_import_works = isinstance(cycle_b.DecoratedBase(value=2), cycle_a.NodeA)
    return {"is_stringized": is_stringized, "annotations": ann, "runtime_base_is_subclass": runtime_import_works}


def framework_early_resolution_demo() -> dict[str, object]:
    """Framework that resolves early before cycle fully loaded must handle failure."""
    early_ok = getattr(cycle_a.EarlyResolvedNode, "_early_resolved", None)
    early_err = getattr(cycle_a.EarlyResolvedNode, "_early_resolution_error", None)
    # Correct approach: resolve lazily with namespace
    lazy_hints = typing.get_type_hints(
        cycle_a.EarlyResolvedNode,
        globalns=vars(cycle_a)
        | {"NodeB": cycle_b.NodeB, "AliasedHelper": cycle_b.HelperB, "HelperB": cycle_b.HelperB},
        include_extras=True,
    )
    return {"early_resolved": early_ok, "early_error_present": early_err is not None, "lazy_keys": sorted(lazy_hints.keys())}


def alias_loss_namespace_demo() -> str:
    return cycle_a.alias_loss_demo()


def cycle_integration_demo() -> dict[str, object]:
    return {
        "with_namespace": resolve_with_namespace(),
        "without_namespace": resolve_without_namespace_failure(),
        "regime": eager_vs_stringized_regime(),
        "framework": framework_early_resolution_demo(),
        "alias_loss": alias_loss_namespace_demo(),
    }
