"""Protocols and structural subtyping (PY-CAN-TYPE-007)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from typing import TypeVar

T = TypeVar("T")

# --- Method protocol ----------------------------------------------------------

class Labelled(Protocol):
    label: str

    def describe(self) -> str: ...


class Widget:
    def __init__(self, label: str) -> None:
        self.label = label

    def describe(self) -> str:
        return f"widget:{self.label}"


class ExplicitLabelled(Labelled):
    def __init__(self, label: str) -> None:
        self.label = label

    def describe(self) -> str:
        return self.label


# --- Property protocol --------------------------------------------------------

class HasCount(Protocol):
    @property
    def count(self) -> int: ...

    @count.setter
    def count(self, value: int) -> None: ...


class Counter:
    def __init__(self, count: int) -> None:
        self._count = count

    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, value: int) -> None:
        self._count = value


# --- Class and static method protocol members ---------------------------------

class WithClassMethod(Protocol):
    @classmethod
    def create(cls, label: str) -> WithClassMethod: ...

    @staticmethod
    def helper(value: int) -> int: ...


class Factory:
    def __init__(self, label: str) -> None:
        self.label = label

    @classmethod
    def create(cls, label: str) -> Factory:
        return cls(label)

    @staticmethod
    def helper(value: int) -> int:
        return value * 2


# --- Generic protocol ---------------------------------------------------------

class Boxed(Protocol[T]):
    value: T

    def get(self) -> T: ...


class IntBox:
    def __init__(self, value: int) -> None:
        self.value = value

    def get(self) -> int:
        return self.value


# --- Runtime-checkable protocol -----------------------------------------------

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...


class Resource:
    def close(self) -> None:
        pass


class NotCloseable:
    pass


def runtime_checkable_demo() -> dict[str, bool]:
    return {
        "resource_is_closeable": isinstance(Resource(), Closeable),
        "not_closeable": not isinstance(NotCloseable(), Closeable),
    }


# --- Implicit and explicit implementations -----------------------------------

# ``Widget`` implicitly implements ``Labelled`` (structural).  ``ExplicitLabelled``
# explicitly inherits from ``Labelled``.  Both satisfy the protocol structurally.

def accepts_labelled(obj: Labelled) -> str:
    return obj.describe()


# --- Runtime signature ignorance variant --------------------------------------

# Protocol checks at runtime are based on attribute presence, not signature
# compatibility.  A class with a ``describe`` method of wrong arity still
# passes ``isinstance`` for a runtime-checkable protocol if the attribute exists.

@runtime_checkable
class Describer(Protocol):
    def describe(self, prefix: str) -> str: ...


class LooseDescriber:
    def describe(self) -> str:  # different signature
        return "loose"


def signature_ignorance_demo() -> bool:
    # Runtime check ignores signature mismatch.
    return isinstance(LooseDescriber(), Describer)


# --- Frozen member set variant -----------------------------------------------

# Protocols have a fixed set of members defined at class creation; adding
# attributes at runtime does not change the protocol's member set.
def frozen_member_set_demo() -> frozenset[str]:
    return frozenset(getattr(Labelled, "__protocol_attrs__", frozenset()))  # type: ignore[attr-defined]


# --- Data-protocol ``issubclass`` variant ------------------------------------
# A runtime-checkable data protocol still rejects ``issubclass`` at runtime;
# we expose the TypeError rather than letting it propagate as an unhandled
# exception.

def data_protocol_issubclass_demo() -> str:
    @runtime_checkable
    class DataProto(Protocol):
        x: int

    class HasX:
        x: int

    try:
        result = issubclass(HasX, DataProto)
        return f"bool:{result}"
    except TypeError as exc:
        return f"TypeError:{exc}"


# --- Dynamic attributes variant -----------------------------------------------

class DynamicAttrs:
    def __getattr__(self, name: str) -> str:
        return f"dynamic:{name}"


def dynamic_attributes_protocol_demo() -> str:
    obj: Labelled = DynamicAttrs()  # type: ignore[assignment]
    return obj.label


# --- Unsafe overlap variant ---------------------------------------------------
# Two protocols overlap on the same member name with incompatible types.
# A class satisfying one protocol's type for that member will be considered
# structurally compatible at runtime but unsound at the static level.

class ProcessorInt(Protocol):
    def process(self, value: int) -> int: ...


class ProcessorStr(Protocol):
    def process(self, value: str) -> str: ...


class IntProcessor:
    def process(self, value: int) -> int:  # type: ignore[override]
        return value * 2


def unsafe_overlap_demo() -> tuple[bool, str]:
    # ``IntProcessor`` satisfies ``ProcessorInt``; using it where
    # ``ProcessorStr`` is expected is the unsafe overlap.
    obj: ProcessorStr = IntProcessor()  # type: ignore[assignment]
    # Runtime call succeeds even though static checker would flag type mismatch.
    return True, str(obj.process("hello"))  # type: ignore[arg-type]


# Keep original disjoint example for reference (not the unsafe case).
class Readable(Protocol):
    def read(self) -> str: ...


class Writable(Protocol):
    def write(self, data: str) -> None: ...


class ReadWrite:
    def read(self) -> str:
        return "data"

    def write(self, data: str) -> None:
        pass
