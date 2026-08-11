"""Legal redefinition and accidental rebinding (PY-CAN-DIAG-019).

Contrasts duplicate definitions/import shadowing with property
accessors, overloads, and conditional definitions.
"""

from __future__ import annotations

from typing import overload


# ---------------------------------------------------------------------------
# Duplicate definitions – last writer wins (legal but accidental)
# ---------------------------------------------------------------------------


def duplicate_function(value: int) -> int:
    """First definition of duplicate_function."""

    return value + 1


def duplicate_function(value: int) -> int:  # noqa: F811  # type: ignore[no-redef]
    """Second definition overwrites the first."""

    return value + 2


class DuplicateClass:
    """First class body."""

    tag = "first"


class DuplicateClass:  # noqa: F811  # type: ignore[no-redef]
    """Second class body replaces the first."""

    tag = "second"


# Import shadowing: name imported then rebound.
from diagnostics_toolkit.warnings_toolkit import ToolkitWarning as ImportedName  # noqa: F401

ImportedName = "shadowed-by-assignment"  # type: ignore[no-redef]


# ---------------------------------------------------------------------------
# Legal redefinition contrasts
# ---------------------------------------------------------------------------


class WithPropertyAccessor:
    """Property accessor contrast – not accidental rebinding."""

    def __init__(self, value: int) -> None:
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, new: int) -> None:
        self._value = new

    @value.deleter
    def value(self) -> None:
        del self._value


@overload
def overloaded_handler(value: int) -> int: ...


@overload
def overloaded_handler(value: str) -> str: ...


def overloaded_handler(value: int | str) -> int | str:
    """Overload stubs followed by implementation – legal redefinition."""

    if isinstance(value, int):
        return value * 2
    return value.upper()


def conditional_definition(flag: bool):  # type: ignore[no-untyped-def]
    """Conditional definition – only one branch defines the name."""

    if flag:

        def handler(x: int) -> int:
            return x + 1

    else:

        def handler(x: int) -> int:
            return x - 1

    return handler


# Class-body replacement counterexample: last writer wins inside class body.
class ClassBodyReplacement:
    first = 1
    first = 2  # type: ignore[no-redef]  # overwrites


def demo_duplicate_binding() -> dict[str, object]:
    """Show duplicate function retains last definition."""

    return {"duplicate_function(1)": duplicate_function(1), "class_tag": DuplicateClass.tag, "shadowed": ImportedName}


def demo_property_vs_rebinding() -> dict[str, object]:
    """Property accessor does not behave like accidental rebinding."""

    obj = WithPropertyAccessor(10)
    before = obj.value
    obj.value = 20
    after = obj.value
    return {"before": before, "after": after, "is_property": isinstance(WithPropertyAccessor.__dict__["value"], property)}


def demo_overload_vs_duplicate() -> dict[str, object]:
    """Overload preserves typing intent; duplicate simply overwrites."""

    return {
        "overload_int": overloaded_handler(21),
        "overload_str": overloaded_handler("hi"),
        "has_overloads": hasattr(overloaded_handler, "__wrapped__") is False,  # overloads use __overloads__ introspection
    }


def demo_conditional() -> dict[str, object]:
    """Conditional definitions pick one branch."""

    inc = conditional_definition(True)
    dec = conditional_definition(False)
    return {"inc(5)": inc(5), "dec(5)": dec(5)}


def all_redefinition_demos() -> dict[str, object]:
    """Collect redefinition demos."""

    return {
        "duplicate": demo_duplicate_binding(),
        "property": demo_property_vs_rebinding(),
        "overload": demo_overload_vs_duplicate(),
        "conditional": demo_conditional(),
        "class_replacement": ClassBodyReplacement.first,
    }
