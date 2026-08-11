"""Private-name mangling and underscore conventions (PY-CAN-BIND-011)."""

from __future__ import annotations

__all__ = ["ManglingBase", "ManglingDerived", "convention_underscores"]


class ManglingBase:
    """Base class with double-underscore attributes subject to mangling."""

    __secret = "base-secret"
    _protected = "base-protected"
    public = "base-public"

    def read_secret(self) -> str:
        return self.__secret

    def read_mangled_explicit(self) -> str:
        return self._ManglingBase__secret


class ManglingDerived(ManglingBase):
    """Subclass reusing the same double-underscore spelling."""

    __secret = "derived-secret"

    def read_derived_secret(self) -> str:
        return self.__secret

    def read_base_secret(self) -> str:
        return self._ManglingBase__secret


def convention_underscores() -> dict[str, str]:
    """Contrast single-underscore convention with dunder exemption."""

    class ConventionHolder:
        _internal = "internal"
        __dunder_exempt__ = "not-mangled"

        def __init__(self) -> None:
            self._instance_internal = "instance"

    holder = ConventionHolder()
    return {
        "class_internal": holder._internal,
        "instance_internal": holder._instance_internal,
        "dunder_exempt": holder.__dunder_exempt__,
    }


def nested_class_context_expression() -> str:
    """Evaluate nested class mangling with each owning context."""

    class Outer:
        __token = "outer-token"

        class Inner:
            __token = "inner-token"

            def read_inner(self) -> str:
                return self.__token

            def read_outer(self) -> str:
                return Outer._Outer__token

    return f"{Outer.Inner().read_inner()}:{Outer.Inner().read_outer()}"


def leading_underscore_class_mangling() -> str:
    """Mangle a double-underscore name on a leading-underscore class."""

    class _LeadingOuter:
        __secret = "leading-secret"

        def reveal(self) -> str:
            return self.__secret

    return _LeadingOuter().reveal()


def reflection_bypass(instance: ManglingBase) -> str:
    """Read a mangled attribute through `getattr` with an explicit name."""

    return getattr(instance, "_ManglingBase__secret")
