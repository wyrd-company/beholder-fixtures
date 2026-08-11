"""Construction protocol (PY-CAN-OBJ-002)."""

from __future__ import annotations

import pickle
from typing import Any


class LoggingMeta(type):
    """Metaclass whose __call__ orchestrates __new__ and __init__."""

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        # Explicitly drive the protocol so code graph sees metaclass __call__.
        obj = cls.__new__(cls, *args, **kwargs)  # type: ignore[misc]
        if isinstance(obj, cls):
            cls.__init__(obj, *args, **kwargs)  # type: ignore[misc]
        return obj


class BaseConstruction(metaclass=LoggingMeta):
    def __new__(cls, value: int = 0) -> BaseConstruction:
        instance = super().__new__(cls)
        instance._init_value = value  # type: ignore[attr-defined]
        return instance

    def __init__(self, value: int = 0) -> None:
        self.value = self._init_value  # type: ignore[attr-defined]
        self.initialized = True


# Immutable subclassing via __new__ (e.g. int-like record).
class ImmutablePoint(tuple):
    """Immutable record subclassing tuple via __new__."""

    def __new__(cls, x: int, y: int) -> ImmutablePoint:
        return super().__new__(cls, (x, y))

    @property
    def x(self) -> int:
        return self[0]

    @property
    def y(self) -> int:
        return self[1]


# Caching via __new__.
class CachedInstance(metaclass=LoggingMeta):
    _cache: dict[int, CachedInstance] = {}

    def __new__(cls, key: int) -> CachedInstance:
        if key in cls._cache:
            return cls._cache[key]
        obj = super().__new__(cls)
        obj.key = key  # type: ignore[attr-defined]
        cls._cache[key] = obj
        return obj

    def __init__(self, key: int) -> None:
        self.seen = True  # idempotent init


# Foreign result from __new__.
class ForeignResult:
    def __new__(cls, use_foreign: bool = False) -> Any:
        if use_foreign:
            return {"foreign": True}
        instance = super().__new__(cls)
        instance.is_foreign = False  # type: ignore[attr-defined]
        return instance

    def __init__(self, use_foreign: bool = False) -> None:
        # When foreign dict was returned, this init should not run; guard.
        if isinstance(self, dict):
            return
        self.use_foreign = use_foreign


# Cooperative bases via super().__new__ / super().__init__.
class CoopA:
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        return super().__new__(cls)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.a_init = True
        super().__init__(*args, **kwargs)  # type: ignore[call-arg]


class CoopB:
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        return super().__new__(cls)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.b_init = True
        super().__init__(*args, **kwargs)  # type: ignore[call-arg]


class CooperativeChild(CoopA, CoopB):
    def __init__(self) -> None:
        super().__init__()


# Bypassed initializer: directly invoke __new__ without __init__.
class BypassedInitializer:
    def __new__(cls, label: str = "default") -> BypassedInitializer:
        obj = super().__new__(cls)
        obj.label = label  # type: ignore[attr-defined]
        return obj

    def __init__(self, label: str = "default") -> None:
        self.label = f"init:{label}"
        self.did_init = True  # type: ignore[attr-defined]


def bypass_initializer_demo() -> BypassedInitializer:
    obj = BypassedInitializer.__new__(BypassedInitializer, "bypassed")
    # __init__ intentionally not called.
    return obj


# __init__ returning non-None must raise TypeError.
class BadInit:
    def __init__(self) -> Any:  # type: ignore[override]
        return 42  # type: ignore[return-value]


def init_non_none_failure_demo() -> str:
    try:
        _ = BadInit()
        return "no-error"
    except TypeError as exc:
        return f"init-return-error:{exc}"


# Pickle reconstruction (via __reduce__ implicitly using __new__).
class PickleableRecord:
    def __init__(self, name: str, score: int) -> None:
        self.name = name
        self.score = score

    def __reduce__(self) -> tuple[Any, ...]:  # type: ignore[override]
        return (self.__class__, (self.name, self.score))


def pickle_roundtrip_demo() -> PickleableRecord:
    original = PickleableRecord("ada", 10)
    data = pickle.dumps(original)
    restored: PickleableRecord = pickle.loads(data)
    return restored
