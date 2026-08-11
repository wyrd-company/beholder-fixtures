"""Copy, replacement, and pickle protocols (PY-CAN-PROT-012)."""

from __future__ import annotations

import copy
import pickle
from dataclasses import dataclass, replace


@dataclass
class LinkedReading:
    value: float
    unit: str
    partner: LinkedReading | None = None

    # replacement API available from Python 3.13 ``copy.replace``
    # dataclasses.replace covers earlier versions and is the primary surface


class SharedAliasGroup:
    """Object graph with shared aliases and a cycle."""

    def __init__(self, value: float) -> None:
        self.value = value
        self.children: list[SharedAliasGroup] = []
        self.tag: str = "root"

    def __copy__(self) -> SharedAliasGroup:
        cls = self.__class__
        cloned = cls.__new__(cls)
        cloned.__dict__.update(self.__dict__)
        cloned.children = list(self.children)
        return cloned

    def __deepcopy__(self, memo: dict[int, object]) -> SharedAliasGroup:
        if id(self) in memo:
            return memo[id(self)]  # type: ignore[return-value]
        cls = self.__class__
        cloned = cls.__new__(cls)
        memo[id(self)] = cloned
        cloned.__dict__ = copy.deepcopy(self.__dict__, memo)
        return cloned

    def __getstate__(self) -> dict[str, object]:
        return self.__dict__.copy()

    def __setstate__(self, state: dict[str, object]) -> None:
        self.__dict__.update(state)

    def __reduce__(self):
        return (_rebuild_shared_alias_group, (self.value, self.tag, self.children))

    def __repr__(self) -> str:
        return f"SharedAliasGroup(value={self.value!r}, tag={self.tag!r})"


def _rebuild_shared_alias_group(value: float, tag: str, children: list) -> SharedAliasGroup:
    obj = SharedAliasGroup(value)
    obj.tag = tag
    obj.children = children
    return obj


class ReducedMeasure:
    """Custom reduction via ``__reduce_ex__``."""

    def __init__(self, value: float, unit: str) -> None:
        self.value = value
        self.unit = unit

    def __reduce_ex__(self, protocol: int):
        return (_rebuild_reduced, (self.value, self.unit, protocol))

    def __repr__(self) -> str:
        return f"ReducedMeasure({self.value!r}, {self.unit!r})"


def _rebuild_reduced(value: float, unit: str, protocol: int) -> ReducedMeasure:
    _ = protocol
    return ReducedMeasure(value, unit)


def copy_cycle_and_alias_demo() -> tuple[bool, bool, bool, bool]:
    """Copy and deep-copy a graph containing both cycle and alias."""

    root = SharedAliasGroup(7.0)
    child = SharedAliasGroup(3.0)
    root.children = [child, child]  # alias: same child twice
    child.children.append(root)  # cycle back to root
    shallow = copy.copy(root)
    deep = copy.deepcopy(root)
    shallow_alias = shallow.children[0] is shallow.children[1]
    shallow_cycle = shallow.children[0].children[0] is shallow
    deep_alias = deep.children[0] is deep.children[1]
    deep_cycle = deep.children[0].children[0] is deep
    return shallow_alias, shallow_cycle, deep_alias, deep_cycle


def pickle_roundtrip_demo() -> tuple[float, bool, bool]:
    """Round-trip a cyclic and aliased graph through pickle."""

    root = SharedAliasGroup(12.0)
    root.tag = "primary"
    child = SharedAliasGroup(2.0)
    root.children = [child, child]  # alias
    child.children.append(root)  # cycle
    data = pickle.dumps(root, protocol=pickle.HIGHEST_PROTOCOL)
    restored: SharedAliasGroup = pickle.loads(data)
    alias_preserved = restored.children[0] is restored.children[1]
    cycle_preserved = restored.children[0].children[0] is restored
    return restored.value, alias_preserved, cycle_preserved


def pickle_protocol_versions_demo() -> list[int]:
    """Serialize with each supported pickle protocol version."""

    obj = ReducedMeasure(5.5, "m")
    versions: list[int] = []
    for proto in range(pickle.HIGHEST_PROTOCOL + 1):
        restored: ReducedMeasure = pickle.loads(pickle.dumps(obj, protocol=proto))
        versions.append(proto if restored.value == obj.value else -1)
    return versions


def local_and_lambda_pickle_failure_demo() -> tuple[str, str, str]:
    """Document local/lambda/resource pickle failures (not executed as untrusted loads).

    Local classes and lambdas cannot be pickled because their qualified name
    is not importable; resources such as ``threading.Lock`` cannot be
    pickled because they hold OS state. These are the expected valid-source
    counterexamples.
    """

    try:
        def make_local():
            class LocalMeasure:
                def __init__(self, v: float) -> None:
                    self.v = v
            return LocalMeasure(1.0)

        obj = make_local()
        pickle.dumps(obj)
        local_result = "no-error"
    except (AttributeError, pickle.PicklingError):
        local_result = "pickling-error"

    try:
        fn = lambda x: x + 1
        pickle.dumps(fn)
        lambda_result = "pickled"
    except (AttributeError, pickle.PicklingError):
        lambda_result = "pickling-error"

    try:
        import threading

        lock = threading.Lock()
        pickle.dumps(lock)
        resource_result = "no-error"
    except (AttributeError, pickle.PicklingError, TypeError, NotImplementedError):
        resource_result = "pickling-error"
    return local_result, lambda_result, resource_result


def untrusted_load_prohibition_note() -> str:
    """Documented negative: do not load untrusted pickle data.

    The fixture never executes ``pickle.loads`` on untrusted input. This
    docstring is the required negative locator; no untrusted payload is
    constructed or loaded.
    """

    return "untrusted pickle loads are prohibited; see docs"


def replacement_api_demo() -> tuple[float, float]:
    """Replacement via ``dataclasses.replace`` and ``copy.replace`` where available."""

    original = LinkedReading(10.0, "kg")
    replaced_dc = replace(original, value=20.0)
    try:
        replaced_copy = copy.replace(original, value=30.0)  # Python 3.13+
    except AttributeError:
        replaced_copy = replace(original, value=30.0)
    return replaced_dc.value, replaced_copy.value
