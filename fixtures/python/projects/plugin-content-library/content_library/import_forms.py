"""Import-statement binding forms (PY-CAN-MOD-005).

Demonstrates which local name each form binds:

- ``import a.b`` binds ``a`` (toplevel) and requires dotted access for ``b``
- ``import a.b as alias`` binds ``alias`` to the leaf
- ``from a import b`` binds ``b``
- ``from a import b as alias`` binds ``alias``

Variants: same module under aliases, dotted-chain access, missing component,
partially initialized package.
"""

from __future__ import annotations

# ``import a.b`` — binds only the top-level package name.
import content_library.registry

# ``import a.b as alias`` — binds the leaf module under the alias.
import content_library.registry as reg_alias

# ``import a.b.c`` dotted chain — leaf accessible via attribute chain.
import content_library.initialized_pkg.child as leaf_alias

# ``from a import b`` — binds the child name directly.
from content_library import registry as from_import_registry

# ``from a import name as alias`` — leaf alias via ``from``.
from content_library.registry import CONTENT_REGISTRY as REG_ALIAS

# ``from package import submodule`` leaf forms.
from content_library.entry_declarations import ContentItem as ItemAlias
from content_library.entry_declarations import create_item

# Same module under two local aliases — identity equality.
import content_library.registry as alias_one
import content_library.registry as alias_two

SAME_MODULE_IS_SAME_OBJECT = alias_one is alias_two is reg_alias is content_library.registry

# Dotted-chain access: ``import content_library.registry`` leaves
# ``content_library.registry.CONTENT_REGISTRY`` reachable via attributes.
DOTTED_CHAIN_REACHABLE = hasattr(content_library, "registry") and hasattr(
    content_library.registry, "CONTENT_REGISTRY"
)

# Leaf alias demonstration: alias points directly to the child.
LEAF_ALIAS_IS_CHILD = leaf_alias.__name__ == "content_library.initialized_pkg.child"

# Missing component — import of a non-existent submodule raises ImportError.
def missing_component_demo() -> str:
    try:
        import content_library.nonexistent_submodule  # type: ignore  # noqa: F401
        return "unexpected-success"
    except ModuleNotFoundError as exc:
        return f"missing-component:{exc.name}"
    except ImportError as exc:  # pragma: no cover
        return f"import-error:{exc}"


# Partially initialized package — observation inside actual initialization.
# ``content_library.partial_pkg``'s ``__init__`` imports its ``child`` while
# ``CHILD_DONE`` not yet set; the child records ``PARTIALLY_INITIALIZED``.
from content_library.partial_pkg import PARTIALLY_DURING_INIT as _partial_during_init
from content_library.partial_pkg.child import PARTIALLY_INITIALIZED as _partial_child, PARENT_IN_SYS_MODULES

PARTIALLY_INITIALIZED_DURING_INIT = _partial_during_init and _partial_child

def partially_initialized_demo() -> dict[str, object]:
    return {
        "parent_partially_during_init": _partial_during_init,
        "child_observes_partial": _partial_child,
        "parent_in_sys_modules_during_child": PARENT_IN_SYS_MODULES,
        "note": "child imported while parent __init__ not yet complete — sys.modules entry exists but CHILD_DONE missing",
    }
