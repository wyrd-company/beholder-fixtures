"""PY-CAN-DYN-005 distribution entry-point plugins."""

from __future__ import annotations

import importlib.metadata as meta


GROUP = "suite.plugins"


def discover_entry_points():
    """Discover after local install (install via pip install --no-index --find-links wheelhouse -e distribution)."""
    try:
        eps = meta.entry_points(group=GROUP)
        return list(eps)
    except TypeError:
        # older fallback
        return meta.entry_points().get(GROUP, [])


def load_entry_point(name: str):
    for ep in discover_entry_points():
        if ep.name == name:
            return ep.load()
    raise KeyError(name)


def private_group_note() -> str:
    return f"{GROUP} is a private group, not a public PyPI group"


def duplicate_names_note() -> str:
    return "duplicate names across distributions would last-wins per installer order"


def dangling_target_note() -> str:
    return "dangling target (import path missing) raises ModuleNotFoundError on load"
