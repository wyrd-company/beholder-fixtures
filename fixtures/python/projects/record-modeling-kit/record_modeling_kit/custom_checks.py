"""Custom instance/subclass checks (PY-CAN-OBJ-019)."""

from __future__ import annotations

import abc
from typing import Any


class DynamicCheckMeta(type):
    """Metaclass with custom __instancecheck__ / __subclasscheck__."""

    def __instancecheck__(cls, instance: Any) -> bool:
        # Dynamic relationship: any object with tag == kind is instance.
        expected = getattr(cls, "expected_tag", None)
        return getattr(instance, "tag", None) == expected if expected is not None else False

    def __subclasscheck__(cls, subclass: type) -> bool:
        expected = getattr(cls, "expected_kind", None)
        return getattr(subclass, "kind", None) == expected if expected is not None else False


class TaggedRecord(metaclass=DynamicCheckMeta):
    expected_tag = "alpha"
    expected_kind = "record"


class AlphaLike:
    tag = "alpha"
    kind = "record"


class BetaLike:
    tag = "beta"
    kind = "other"


# ABC variant with __subclasshook__ and caching.
class ShapeHook(abc.ABC):
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        if cls is ShapeHook:
            if hasattr(subclass, "area"):
                return True
        return NotImplemented


class HasArea:
    def area(self) -> float:
        return 1.0


class NoArea:
    pass


def instancecheck_demo() -> tuple[bool, bool]:
    return isinstance(AlphaLike(), TaggedRecord), isinstance(BetaLike(), TaggedRecord)


def subclasscheck_demo() -> tuple[bool, bool]:
    return issubclass(AlphaLike, TaggedRecord), issubclass(BetaLike, TaggedRecord)


def abc_caching_demo() -> tuple[bool, bool]:
    # ABC caches subclass checks; verify caching still correct after first call.
    first = issubclass(HasArea, ShapeHook)
    second = issubclass(HasArea, ShapeHook)
    return first, second


def recursive_check_demo() -> str:
    # Recursive check guard: metaclass hook that would recurse if not careful.
    class SafeMeta(type):
        def __subclasscheck__(cls, sub: type) -> bool:
            # Avoid recursion by not calling issubclass within itself without guard.
            return sub is SafeMeta or super().__subclasscheck__(sub)  # type: ignore[misc]

    class Safe(metaclass=SafeMeta):
        pass

    class Child(Safe):
        pass

    return str(issubclass(Child, Safe))


def parameterized_generic_restriction_demo() -> str:
    # Parameterized generics like list[int] cannot be used with custom checks directly.
    try:
        # list[int] as type in issubclass raises TypeError.
        _ = issubclass(list[int], list)  # type: ignore[arg-type]
        return "no-error"
    except TypeError as exc:
        return f"generic-restriction:{exc}"


def static_tools_do_not_infer_demo() -> str:
    # Static tools cannot infer arbitrary hook; runtime check succeeds though.
    obj = AlphaLike()
    # At runtime isinstance passes, but static checker would not know tag == expected_tag.
    return f"runtime-{isinstance(obj, TaggedRecord)}-static-unknown"
