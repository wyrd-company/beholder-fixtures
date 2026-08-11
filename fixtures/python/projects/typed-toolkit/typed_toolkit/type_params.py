"""Type parameters (PY-CAN-TYPE-005)."""

from __future__ import annotations

from typing import Generic, TypeVar
from typing import TypeVar as LegacyTypeVar

# --- Legacy TypeVar forms -----------------------------------------------------

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)
BoundedVar = TypeVar("BoundedVar", bound=str)
ConstrainedVar = TypeVar("ConstrainedVar", int, str)


def legacy_bounded(value: BoundedVar) -> BoundedVar:
    return value


def legacy_constrained(value: ConstrainedVar) -> str:
    if isinstance(value, int):
        return str(value)
    return value


def legacy_covariant(items: list[T_co]) -> T_co | None:
    return items[0] if items else None


# --- Legacy Generic form for explicit variance (assigned) ---------------------

T_co2 = TypeVar("T_co2", covariant=True)
T_contra2 = TypeVar("T_contra2", contravariant=True)


class CovariantBox(Generic[T_co2]):
    def __init__(self, value: T_co2) -> None:
        self.value = value

    def get(self) -> T_co2:
        return self.value


class ContravariantBox(Generic[T_contra2]):
    def __init__(self) -> None:
        pass

    def consume(self, value: T_contra2) -> None:
        pass


def explicit_variance_demo() -> tuple[bool, bool]:
    return CovariantBox.__parameters__[0].__covariant__, ContravariantBox.__parameters__[0].__contravariant__  # type: ignore[attr-defined]


# --- PEP 695 new syntax (inferred variance) ----------------------------------

def pep695_generic_function[T](value: T) -> T:
    return value


class Pep695Box[T]:
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value


class BoundedBox[T: str]:
    def __init__(self, value: T) -> None:
        self.value = value


class ConstrainedBox[T: (int, str)]:
    def __init__(self, value: T) -> None:
        self.value = value


# Inferred variance demonstration: type checker infers variance from usage.
class InferredReadOnlyBox[T]:
    def __init__(self, value: T) -> None:
        self._value = value

    def get(self) -> T:
        return self._value


def inferred_variance_demo() -> tuple[object, ...]:
    params = getattr(InferredReadOnlyBox, "__type_params__", ())  # type: ignore[attr-defined]
    return tuple(getattr(p, "__name__", str(p)) for p in params)  # type: ignore[arg-type]


# --- PEP 696 defaults (Python 3.13+) -----------------------------------------

# Defaults in new syntax; ordering: non-defaults before defaults.
class WithDefault[T = str]:
    def __init__(self, value: T | None = None) -> None:
        self.value = value


class MultiParam[A, B = int, C = str]:
    def __init__(self, a: A, b: B | None = None, c: C | None = None) -> None:
        self.a = a
        self.b = b
        self.c = c


# Generic function with default type parameter
def with_default_param[T = int](value: T | None = None) -> T | None:
    return value


# Ordering of defaults: required before defaulted.
type PairWithDefault[A, B = str] = tuple[A, B]


# --- Bound versus constraints contrast ---------------------------------------

# Bound: single upper bound (``bound=``).  Constraint: enumerated choices.
BoundedOnly = TypeVar("BoundedOnly", bound=float)
ConstrainedOnly = TypeVar("ConstrainedOnly", int, float, str)


# --- Substitution not runtime-enforced ---------------------------------------

def substitution_not_enforced_demo() -> str:
    box: Pep695Box[int] = Pep695Box("not-an-int")  # type: ignore[assignment]
    # At runtime the generic specialization is erased; no enforcement.
    return str(box.get())


# --- Lexical scope of type parameters ----------------------------------------

def lexical_scope_demo() -> str:
    # Type parameters are lexically scoped to their generic.
    def inner[U](value: U) -> U:
        return value

    return inner("scoped")


# --- Ordering of defaults demo -----------------------------------------------

def ordering_defaults_demo() -> MultiParam[int]:
    # ``MultiParam[int]`` fills ``A`` with int, uses defaults for B, C.
    return MultiParam(42)
