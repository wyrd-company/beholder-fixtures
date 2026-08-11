"""Definition-time defaults (PY-CAN-CALL-002)."""

from __future__ import annotations

OUTER_LABEL = "initial-label"


def collect_with_shared_default(items: list[str] = []) -> list[str]:  # noqa: B006 — shared mutable variant
    """Shared mutable default is evaluated once at definition time."""

    items.append("parcel")
    return items


def collect_with_sentinel(items: list[str] | None = None) -> list[str]:
    """Sentinel correction avoids the shared-default pitfall."""

    if items is None:
        items = []
    items.append("parcel")
    return items


def capture_outer_label(label: str = OUTER_LABEL) -> str:
    """Default captures the outer name's value at definition time."""

    return label


# Rebind the outer name after function definition; default keeps original.
OUTER_LABEL = "rebound-label"


def default_ordering_rules(
    base: str,
    optional: str = "default",
    *extras: str,
    required_kw: str,
    optional_kw: str = "kw-default",
    **attrs: str,
) -> dict[str, object]:
    """Show ordering: non-default, default, *args, keyword-only required, keyword-only default, **kwargs."""

    return {
        "base": base,
        "optional": optional,
        "extras": list(extras),
        "required_kw": required_kw,
        "optional_kw": optional_kw,
        "attrs": dict(attrs),
    }


def defaults_cannot_reference_call_time_params() -> tuple[str, str]:
    """Defaults cannot name call-time parameters; annotation policy is separate."""

    # Default expression is evaluated at definition time in its own scope.
    # It cannot reference a later parameter name.
    captured = OUTER_LABEL  # value at definition time, not at call time

    def inner(value: str = captured, *, label: str = captured) -> tuple[str, str]:
        return value, label

    first = inner()[0]
    second = inner("override")[0]
    return first, second


def annotation_evaluation_policy() -> dict[str, object]:
    """Annotations are evaluated separately from defaults.

    In ``from __future__ import annotations`` the annotations are stored as
    strings, but defaults are still evaluated at definition time.
    """

    token = "annotation-token"

    def tagged(value: str, label: str = token) -> str:  # label default captured now
        return f"{value}:{label}"

    # Annotation is not evaluated eagerly when stringized.
    return {
        "default": tagged(),
        "annotation": tagged.__annotations__,
        "qualname": tagged.__qualname__,
    }
