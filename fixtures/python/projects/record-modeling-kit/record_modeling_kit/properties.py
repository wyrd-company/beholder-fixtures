"""Properties (PY-CAN-OBJ-007)."""

from __future__ import annotations

import abc
import functools


class ManagedRecord:
    def __init__(self, title: str, score: int) -> None:
        self._title = title
        self._score = score

    # Read-only property.
    @property
    def title(self) -> str:
        return self._title

    # Read-write property with validation.
    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        if value < 0:
            raise ValueError("score must be non-negative")
        self._score = value

    @score.deleter
    def score(self) -> None:
        del self._score

    # Property whose setter creates a new property object (fluent).
    @property
    def tag(self) -> str:
        return getattr(self, "_tag", "untagged")

    @tag.setter
    def tag(self, value: str) -> None:
        self._tag = value.upper()

    @tag.deleter
    def tag(self) -> None:
        self._tag = "untagged"


class InheritedRecord(ManagedRecord):
    @ManagedRecord.score.getter  # type: ignore[attr-defined]
    def score(self) -> int:  # type: ignore[override]
        return super().score + 10


class AbstractRecord(abc.ABC):
    @property
    @abc.abstractmethod
    def identifier(self) -> str: ...

    @identifier.setter
    @abc.abstractmethod
    def identifier(self, value: str) -> None: ...

    @identifier.deleter
    @abc.abstractmethod
    def identifier(self) -> None: ...  # type: ignore[no-redef]


class ConcreteRecord(AbstractRecord):
    def __init__(self, identifier: str) -> None:
        self._identifier = identifier

    @property
    def identifier(self) -> str:
        return self._identifier

    @identifier.setter
    def identifier(self, value: str) -> None:
        self._identifier = value

    @identifier.deleter
    def identifier(self) -> None:
        del self._identifier


class ErrorRaising:
    @property
    def fragile(self) -> str:
        raise RuntimeError("fragile access failed")


def property_inheritance_demo() -> int:
    rec = InheritedRecord("demo", 5)
    return rec.score  # 15 via override


def setter_creates_new_property_demo() -> str:
    # Accessor: p = ManagedRecord.score; p2 = p.setter(new_setter) creates new property.
    p = ManagedRecord.score  # type: ignore[attr-defined]
    assert isinstance(p, property)

    def new_setter(self: ManagedRecord, value: int) -> None:
        self._score = value * 2

    p2 = p.setter(new_setter)
    return type(p2).__name__


def class_access_demo() -> str:
    # Access via class returns property object; via instance returns computed value.
    cls_attr = ManagedRecord.__dict__["title"]
    inst = ManagedRecord("hello", 1)
    return f"{type(cls_attr).__name__}:{inst.title}"


def cached_property_contrast_demo() -> tuple[str, str]:
    class WithCached:
        def __init__(self) -> None:
            self.calls = 0

        @functools.cached_property
        def computed(self) -> str:
            self.calls += 1
            return f"cached-{self.calls}"

        @property
        def normal(self) -> str:
            self.calls += 1
            return f"normal-{self.calls}"

    obj = WithCached()
    first_cached = obj.computed
    second_cached = obj.computed
    first_normal = obj.normal
    second_normal = obj.normal
    return f"{first_cached}/{second_cached}", f"{first_normal}/{second_normal}"


def error_raising_demo() -> str:
    obj = ErrorRaising()
    try:
        _ = obj.fragile
        return "no-error"
    except RuntimeError as exc:
        return f"property-error:{exc}"


def deletable_demo() -> str:
    rec = ManagedRecord("del-demo", 3)
    del rec.score
    try:
        _ = rec.score
        return "no-error"
    except AttributeError as exc:
        return f"deleted:{exc}"
