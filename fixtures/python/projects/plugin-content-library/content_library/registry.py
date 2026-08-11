"""Content registry populated at import time (PY-CAN-MOD-012).

``CONTENT_REGISTRY`` is mutated as a side effect of importing modules
that call :func:`register_content`.  First-import-only semantics are
demonstrated by the fact that ``register_content`` is not re-executed
on cached imports.  See ``import_time_registry.py`` for ordering and
double-execution notes.
"""

from __future__ import annotations

CONTENT_REGISTRY: dict[str, dict[str, object]] = {}

REGISTRY_ORDER: list[str] = []


def register_content(name: str, meta: dict[str, object]) -> None:
    CONTENT_REGISTRY[name] = meta
    REGISTRY_ORDER.append(name)


def get_registry_snapshot() -> dict[str, dict[str, object]]:
    return dict(CONTENT_REGISTRY)
