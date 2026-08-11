"""Absolute and explicit-relative resolution (PY-CAN-MOD-006).

Resolves sibling and parent imports against a same-named top-level candidate.

Structure:

- Top-level candidate (would shadow): ``content_library.top_sibling`` (see
  ``content_library/top_sibling.py``) versus
  ``content_library.resolution_pkg.sibling_a``.
- This module uses absolute ``import content_library.resolution_pkg.sibling_a``
  and explicit-relative ``from .. import sibling_a`` and ``from . import ...``
  to reach siblings.

Variants: beyond-top-level failure, direct-script missing parent, depth
refactor, aliases.
"""

from __future__ import annotations

# Absolute import — fully qualified, unambiguous.
import content_library.resolution_pkg.sibling_a as abs_sibling_a

# Explicit-relative sibling import.
from .. import sibling_a as rel_sibling_a

# Explicit-relative parent import (one level up).
from ..sibling_b import VALUE as parent_value

# Alias variant for relative import.
from ..sibling_a import func_a as sibling_func_alias

# The package of this module when imported normally.
PACKAGE_CONTEXT = __package__  # "content_library.resolution_pkg.sub"


def resolve_variants() -> dict[str, object]:
    return {
        "abs_is_rel": abs_sibling_a is rel_sibling_a,
        "parent_value": parent_value,
        "alias_result": sibling_func_alias(),
        "package": PACKAGE_CONTEXT,
    }


def beyond_top_level_demo() -> str:
    """Attempt a relative import beyond the top-level package."""
    try:
        # ``....`` from sub (depth 3) escapes content_library and must fail.
        from .... import registry  # type: ignore  # noqa: F401

        return "unexpected-beyond-success"
    except ImportError as exc:
        return f"beyond-top-level-failed:{exc.__class__.__name__}"
    except ValueError as exc:
        # CPython raises ValueError "attempted relative import beyond top-level package"
        return f"beyond-top-level-failed:ValueError:{exc}"


def direct_script_missing_parent_demo() -> str:
    """When run as ``__main__``, ``__package__`` is None so relative fails."""
    # Simulate the direct-script environment by inspecting what would happen.
    # The actual failure occurs when ``python content_library/resolution_pkg/sub/deep_module.py``
    # is executed; here we document the shape without spawning.
    if __package__ is None or __package__ == "":
        return "direct-script-no-parent"
    # In normal import, parent exists, so we show that relative would succeed.
    return "imported-has-parent"
