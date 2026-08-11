"""Abstract and virtual subclasses (PY-CAN-OBJ-010)."""

from __future__ import annotations

import abc
from typing import Protocol, runtime_checkable


class DataSink(abc.ABC):
    @abc.abstractmethod
    def write(self, data: str) -> None: ...

    @property
    @abc.abstractmethod
    def name(self) -> str: ...

    @classmethod
    @abc.abstractmethod
    def kind(cls) -> str: ...


class FileSink(DataSink):
    def __init__(self, name: str) -> None:
        self._name = name
        self.written: list[str] = []

    def write(self, data: str) -> None:
        self.written.append(data)

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def kind(cls) -> str:
        return "file"


# Registered virtual subclass (does not inherit).
class NetworkSink:
    def write(self, data: str) -> None:
        self.sent = data  # type: ignore[attr-defined]

    @property
    def name(self) -> str:
        return "network"

    @classmethod
    def kind(cls) -> str:
        return "network"


DataSink.register(NetworkSink)


# __subclasshook__ based virtual subclass.
class HookedShape(abc.ABC):
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        if cls is HookedShape:
            if any("area" in B.__dict__ for B in subclass.__mro__):
                return True
        return NotImplemented

    @abc.abstractmethod
    def area(self) -> float: ...


class Square:
    def area(self) -> float:
        return 4.0


class NoArea:
    pass


# Decorator order: correct order is @property then @abstractmethod.
class OrderA(abc.ABC):
    @property
    @abc.abstractmethod
    def label(self) -> str: ...


# Protocol contrast (structural, not ABC).
@runtime_checkable
class Writable(Protocol):
    def write(self, data: str) -> None: ...


def concrete_subclass_demo() -> str:
    sink = FileSink("demo")
    sink.write("hello")
    return sink.written[0]


def virtual_subclass_demo() -> tuple[bool, bool, bool]:
    inst = NetworkSink()
    is_virtual_instance = isinstance(inst, DataSink)
    is_virtual_sub = issubclass(NetworkSink, DataSink)
    # Virtual subclass does not inherit DataSink members via MRO.
    has_write_in_mro = any("write" in B.__dict__ for B in NetworkSink.__mro__ if B is not DataSink)
    return is_virtual_instance, is_virtual_sub, has_write_in_mro


def subclasshook_demo() -> tuple[bool, bool]:
    return issubclass(Square, HookedShape), issubclass(NoArea, HookedShape)


def instantiation_failure_demo() -> str:
    try:
        _ = DataSink()  # type: ignore[abstract]
        return "no-error"
    except TypeError as exc:
        return f"abstract-instantiation:{exc}"


def cache_invalidation_demo() -> bool:
    # ABC caches subclass checks; after register, cache reflects new relation.
    class Temp:  # noqa: N801
        pass

    before = issubclass(Temp, DataSink)
    DataSink.register(Temp)
    after = issubclass(Temp, DataSink)
    return (not before) and after


def decorator_order_demo() -> tuple[str, bool]:
    # Correct order succeeds; reversed order (abstractmethod before property) raises AttributeError.
    ok = issubclass(OrderA, abc.ABC)
    try:
        class OrderB(abc.ABC):
            @abc.abstractmethod  # type: ignore[misc]
            @property
            def label(self) -> str: ...  # type: ignore[misc]

        _ = OrderB
        reversed_ok: str = "no-error"
    except AttributeError as exc:
        reversed_ok = f"decorator-order-error:{exc}"
    return reversed_ok, ok


def protocol_contrast_demo() -> tuple[bool, bool]:
    inst = NetworkSink()
    return isinstance(inst, DataSink), isinstance(inst, Writable)
