"""Method descriptor forms (PY-CAN-CALL-006)."""

from __future__ import annotations

from types import FunctionType, MethodType
from typing import Any


class Toolkit:
    """Container exposing normal, static, and class descriptor forms."""

    prefix = "parcel"

    def normal(self, label: str) -> str:
        """Normal method whose descriptor binds ``self``."""

        return f"{self.prefix}:{label}"

    @staticmethod
    def via_static(label: str) -> str:
        """Static method without binding."""

        return f"static:{label}"

    @classmethod
    def via_class(cls, label: str) -> str:
        """Class method bound to the class."""

        return f"class:{cls.__name__}:{label}"


def access_through_class_and_instance() -> dict[str, object]:
    """Access each descriptor form through class and instance and compare receivers."""

    obj = Toolkit()
    return {
        "class_normal": Toolkit.normal,
        "instance_normal": obj.normal,
        "class_static": Toolkit.via_static,
        "instance_static": obj.via_static,
        "class_method": Toolkit.via_class,
        "instance_method": obj.via_class,
        "instance_normal_is_bound": isinstance(obj.normal, MethodType),
        "instance_static_is_function": isinstance(obj.via_static, FunctionType) or callable(obj.via_static),
        "class_method_receiver": Toolkit.via_class.__self__,  # type: ignore[attr-defined]
        "instance_method_receiver": obj.via_class.__self__,  # type: ignore[attr-defined]
    }


def raw_class_dictionary() -> dict[str, Any]:
    """Inspect raw class ``__dict__`` where descriptors are still unbound."""

    d = Toolkit.__dict__
    return {
        "normal": d["normal"],
        "static": d["via_static"],
        "class": d["via_class"],
        "normal_type": type(d["normal"]).__name__,
        "static_type": type(d["via_static"]).__name__,
        "class_type": type(d["via_class"]).__name__,
    }


def fresh_bound_method_objects() -> bool:
    """Each attribute read of a normal method produces a fresh bound-method object."""

    obj = Toolkit()
    a = obj.normal
    b = obj.normal
    return a is not b and a == b and a.__func__ is b.__func__  # type: ignore[attr-defined]


def instance_assigned_function() -> dict[str, object]:
    """Instance-assigned function shadows the class descriptor."""

    obj = Toolkit()

    def override(label: str) -> str:
        return f"override:{label}"

    obj.normal = override  # type: ignore[method-assign]
    return {
        "via_instance": obj.normal("parcel"),
        "is_override": obj.normal is override,
        "class_still_descriptor": isinstance(Toolkit.__dict__["normal"], FunctionType),
    }


def decorator_order() -> dict[str, str]:
    """Contrast decorator stacking order for static and class methods."""

    class Ordered:
        @staticmethod
        @property
        def _order_note() -> str:  # type: ignore[no-redef]
            return "static-wraps-property"

        @classmethod
        def check_class(cls) -> str:
            return cls.__name__

    return {
        "ordered_check": Ordered.check_class(),
    }
