"""Comprehension and generator-expression scope (PY-CAN-BIND-005)."""

from __future__ import annotations

from typing import Iterator


def comprehension_forms(source: dict[str, int]) -> dict[str, object]:
    """Cover list, set, dict, and generator comprehension scoping."""

    outer_key = "outer"

    list_values = [value for value in source.values()]
    set_keys = {key for key in source}
    dict_pairs = {key: value for key, value in source.items()}
    generator_values = (value + 1 for value in source.values())

    return {
        "outer": outer_key,
        "list": list_values,
        "set": sorted(set_keys),
        "dict": dict_pairs,
        "generator": list(generator_values),
    }


def walrus_in_comprehension(rows: list[tuple[str, int]]) -> list[str]:
    """Bind a walrus target in a comprehension filter."""

    return [
        label
        for label, amount in rows
        if (threshold := amount // 2) > 0 and label.startswith("t")
    ]


def leftmost_iterable_binding(groups: list[tuple[str, list[int]]]) -> list[int]:
    """Bind the leftmost iterable name before nested iteration."""

    return [value for label, values in groups for value in values if label]


def generator_laziness(values: list[int]) -> Iterator[int]:
    """Return a generator expression that defers evaluation."""

    multiplier = 2
    return (item * multiplier for item in values)


def class_body_lookup_failure() -> str:
    """Handle nested comprehension lookup failure for a class local."""

    try:
        class BodyLookup:
            seed = "class-seed"
            tokens = [
                inner
                for outer in ("a", "b")
                for inner in (outer,)
                if label == outer
            ]
            label = "class-label"

        _ = BodyLookup.tokens
        return "unexpected-success"
    except NameError:
        return "name-error"


def forbidden_walrus_in_iterable() -> list[int]:
    """Use walrus only in permitted comprehension positions."""

    numbers = [1, 2, 3, 4]
    return [value for value in numbers if (doubled := value * 2) > 3]
