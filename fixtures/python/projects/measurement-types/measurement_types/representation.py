"""Representation and conversion (PY-CAN-PROT-008)."""

from __future__ import annotations

import reprlib


class LabeledMeasure:
    """Measurement with ``__repr__``, ``__str__``, ``__format__``, and ``__bytes__``."""

    def __init__(self, value: float, unit: str) -> None:
        self.value = value
        self.unit = unit

    def __repr__(self) -> str:
        return f"LabeledMeasure(value={self.value!r}, unit={self.unit!r})"

    def __str__(self) -> str:
        return f"{self.value} {self.unit}"

    def __format__(self, spec: str) -> str:
        if spec == "short":
            return f"{self.value:g}{self.unit[0]}"
        if spec == "" or spec == "full":
            return f"{self.value} {self.unit}"
        raise ValueError(f"unsupported format: {spec!r}")

    def __bytes__(self) -> bytes:
        return f"{self.value} {self.unit}".encode("utf-8")


class RecursiveMeasure:
    """Demonstrate recursive ``repr`` guarding with ``reprlib.recursive_repr``."""

    def __init__(self) -> None:
        self.partner: RecursiveMeasure | None = None

    @reprlib.recursive_repr()
    def __repr__(self) -> str:
        if self.partner is not None:
            return f"RecursiveMeasure(partner={self.partner!r})"
        return "RecursiveMeasure()"


def fstring_conversion_flags(value: LabeledMeasure) -> dict[str, str]:
    """Show ``!s``, ``!r``, ``!a`` conversion before formatting."""

    return {
        "str_flag": f"{value!s}",
        "repr_flag": f"{value!r}",
        "ascii_flag": f"{value!a}",
        "format_short": f"{value:short}",
        "conversion_then_format": f"{value!r:}",
    }


def required_return_type_demo() -> tuple[str, str, bytes]:
    """Verify required return types for the conversion protocols."""

    obj = LabeledMeasure(12.5, "kg")
    return repr(obj), str(obj), bytes(obj)


def unsupported_format_demo() -> str:
    """Trigger unsupported format handling."""

    obj = LabeledMeasure(3.0, "m")
    try:
        format(obj, "unknown")
        return "no-error"
    except ValueError:
        return "value-error"


def recursive_repr_demo() -> str:
    """Produce a recursive structure and format it without recursion error."""

    a = RecursiveMeasure()
    b = RecursiveMeasure()
    a.partner = b
    b.partner = a
    return repr(a)


def conversion_before_formatting_demo() -> str:
    """Apply conversion then format spec via f-string."""

    obj = LabeledMeasure(7.0, "s")
    # ``!r`` applies repr conversion before the format spec is interpreted
    return f"{obj!r:}"
