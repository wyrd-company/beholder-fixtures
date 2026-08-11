"""String-mediated attribute and namespace access (PY-CAN-DYN-003)."""

from __future__ import annotations


class CatalogEntry:
    catalog_label = "generic"
    region = "default"


# Constant-name resolution.
def feature_probe(obj: object, name: str, default: object = None) -> object:
    """Use hasattr/getattr with constant and default for feature probing."""
    if hasattr(obj, name):
        return getattr(obj, name, default)
    return default


# Computed name variant plus setattr/delattr/hasattr.
def computed_attribute(obj: object, base: str, suffix: str, value: object | None = None) -> object | None:
    name = f"{base}_{suffix}"
    if value is not None:
        setattr(obj, name, value)
        return getattr(obj, name)
    if hasattr(obj, name):
        result = getattr(obj, name)
        delattr(obj, name)
        # Latent typo counterexample: missing attribute after deletion.
        return result if not hasattr(obj, name) else None
    # Missing attribute with explicit default.
    return getattr(obj, name, None)


# vars() and globals() variants.
MODULE_EXPORT = "exported-value"
_dynamic_entries: dict[str, object] = {}


def dynamic_export(name: str, value: object) -> None:
    """Publish into module namespace via globals() and track via vars()."""
    globals()[name] = value
    _dynamic_entries[name] = value


def resolve_via_vars(obj: object) -> dict[str, object]:
    """Snapshot attributes through vars() and globals()."""
    own = dict(vars(obj)) if hasattr(obj, "__dict__") else {}
    module_snapshot = {k: v for k, v in globals().items() if not k.startswith("_")}
    own["module_keys_sample"] = sorted(module_snapshot.keys())[:3]
    return own


# Dynamic export read-back with hasattr default.
def consume_dynamic_export(name: str) -> object:
    return getattr(CatalogEntry, name, None) if hasattr(CatalogEntry, name) else globals().get(name)


# Missing / latent typo counterexample: computed target that never exists.
def missing_attribute_demo() -> tuple[bool, object]:
    candidate = "nonexistent_field_xyz"
    exists = hasattr(CatalogEntry, candidate)
    value = getattr(CatalogEntry, candidate, "fallback")
    return exists, value


# Computed target unresolved statically: name built at runtime.
def dispatch_by_name(target: object, method_name: str, *args: object) -> object:
    fn = getattr(target, method_name)  # noqa: B009 — string-mediated dispatch is the point
    return fn(*args) if callable(fn) else fn
