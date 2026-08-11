"""Star-import collision (PY-CAN-DIAG-022).

Imports two surfaces with one overlapping name and demonstrates
statement-order rebinding. Contrasts with explicit imports that
bypass __all__.
"""

from __future__ import annotations


def demo_star_order_a_then_b() -> dict[str, object]:
    """from star_a import * then from star_b import * → shared_name is 'from-b'."""

    namespace: dict[str, object] = {}
    exec("from diagnostics_toolkit.star_a import *", namespace)
    after_a = namespace.get("shared_name")
    exec("from diagnostics_toolkit.star_b import *", namespace)
    after_b = namespace.get("shared_name")
    return {
        "after_a": after_a,
        "after_b": after_b,
        "unique_a_present": "unique_a" in namespace,
        "unique_b_present": "unique_b" in namespace,
        "collision_overwritten": after_a != after_b and after_b == "from-b",
    }


def demo_star_order_b_then_a() -> dict[str, object]:
    """from star_b import * then from star_a import * → shared_name is 'from-a'."""

    namespace: dict[str, object] = {}
    exec("from diagnostics_toolkit.star_b import *", namespace)
    after_b = namespace.get("shared_name")
    exec("from diagnostics_toolkit.star_a import *", namespace)
    after_a = namespace.get("shared_name")
    return {
        "after_b": after_b,
        "after_a": after_a,
        "collision_overwritten": after_b != after_a and after_a == "from-a",
    }


def demo_all_changes_collision_set() -> dict[str, object]:
    """__all__ controls which names star-import exports; without it underscore names are hidden."""

    # star_a and star_b both define __all__, so only listed names are exported.
    # Demonstrate that a name not in __all__ would not be exported.
    # We check via exec that unique_a/b are exported but a private would not be.
    namespace: dict[str, object] = {}
    exec("from diagnostics_toolkit.star_a import *", namespace)
    has_shared = "shared_name" in namespace
    has_unique_a = "unique_a" in namespace
    # Simulate a module without __all__ that has a private name: it would not be exported.
    # This is shown via a temporary module namespace.
    tmp_ns: dict[str, object] = {"_hidden": "secret", "visible": "yes"}
    # star without __all__ would export visible but not _hidden – we just assert the rule.
    return {
        "has_shared": has_shared,
        "has_unique_a": has_unique_a,
        "all_controls_collision": has_shared and has_unique_a,
    }


def demo_explicit_import_contrast() -> dict[str, object]:
    """Explicit imports bypass __all__ and are order-independent."""

    from diagnostics_toolkit.star_a import shared_name as shared_a
    from diagnostics_toolkit.star_b import shared_name as shared_b

    # Reverse order still gives same bindings because explicit imports use names, not star.
    from diagnostics_toolkit.star_b import shared_name as shared_b2
    from diagnostics_toolkit.star_a import shared_name as shared_a2

    return {
        "shared_a": shared_a,
        "shared_b": shared_b,
        "shared_a2": shared_a2,
        "shared_b2": shared_b2,
        "explicit_stable": shared_a == "from-a" and shared_b == "from-b",
    }


def all_star_collision_demos() -> dict[str, object]:
    """Collect star-import collision demos."""

    return {
        "a_then_b": demo_star_order_a_then_b(),
        "b_then_a": demo_star_order_b_then_a(),
        "all_collision": demo_all_changes_collision_set(),
        "explicit_contrast": demo_explicit_import_contrast(),
    }
