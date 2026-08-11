"""Star imports and ``__all__`` demonstration (PY-CAN-MOD-008).

This module performs star imports at module scope to show each variant.
Non-blocking variants are wrapped in functions so the module remains importable
even when a variant would raise.

Variants covered:

- explicit ``__all__`` (``explicit_all``)
- computed ``__all__`` (``computed_all``)
- missing-name in ``__all__`` (``missing_name_all`` — failure case)
- absent ``__all__`` underscore fallback (``no_all``)
- package child import via star
- multiple-star collision (``collision_a`` then ``collision_b``)
- explicit imports bypass ``__all__``
- module-scope restriction (star inside function is syntax error)
"""

from __future__ import annotations

# Explicit __all__: only public_a/public_b are star-exported.
from content_library.star_pkg.explicit_all import *  # noqa: F403

# Computed __all__: alpha/beta/gamma exported, _internal not.
from content_library.star_pkg.computed_all import *  # noqa: F403

# Absent __all__: public_one/public_two/ANOTHER exported, _hidden not.
from content_library.star_pkg.no_all import *  # noqa: F403

# Multiple-star collision: common from collision_b overwrites collision_a.
from content_library.star_pkg.collision_a import *  # noqa: F403
from content_library.star_pkg.collision_b import *  # noqa: F403

# Capture exported names for inspection (relying on what star left behind).
STAR_EXPORTED = {
    "public_a": public_a if "public_a" in globals() else None,  # type: ignore
    "public_b": public_b if "public_b" in globals() else None,  # type: ignore
    "alpha": alpha if "alpha" in globals() else None,  # type: ignore
    "common_final": common if "common" in globals() else None,  # type: ignore
}

# Explicit import bypasses __all__: _private is not star-exported but directly importable.
from content_library.star_pkg.explicit_all import _private  # noqa: F401


def missing_name_star_failure() -> str:
    """Importing ``missing_name_all`` via star raises AttributeError."""
    try:
        exec("from content_library.star_pkg.missing_name_all import *", {})  # noqa: S102
        return "unexpected-success"
    except AttributeError as exc:
        return f"missing-name-star-failed:{exc}"
    except ImportError as exc:
        return f"missing-name-star-failed-import:{exc}"


def module_scope_restriction_note() -> str:
    """Star imports are only allowed at module scope; function scope is syntax error."""
    # The following would be SyntaxError if uncommented:
    # def inner():
    #     from .explicit_all import *  # noqa: F403
    return "star-only-at-module-scope"


def underscore_fallback_check() -> dict[str, bool]:
    return {
        "private_not_in_star": "_private" not in STAR_EXPORTED or STAR_EXPORTED.get("_private") is None,
        "hidden_not_exported": "_hidden" not in globals(),
    }
