"""Weak references and finalization (PY-CAN-OBJ-017)."""

from __future__ import annotations

import gc
import weakref
from typing import Any


class WeakRefDemo:
    def __init__(self, label: str) -> None:
        self.label = label


class SlottedWeak:
    __slots__ = ("value", "__weakref__")

    def __init__(self, value: str) -> None:
        self.value = value


class SlottedNoWeak:
    __slots__ = ("value",)

    def __init__(self, value: str) -> None:
        self.value = value


def weak_reference_demo() -> bool:
    # Non-timing check: after deletion and gc, ref returns None.
    obj = WeakRefDemo("temp")
    ref = weakref.ref(obj)
    assert ref() is obj
    del obj
    gc.collect()
    return ref() is None


def weak_collection_demo() -> tuple[bool, bool]:
    # WeakKeyDictionary and WeakSet with non-timing checks.
    key = WeakRefDemo("key")
    wkd: weakref.WeakKeyDictionary[WeakRefDemo, str] = weakref.WeakKeyDictionary()
    wkd[key] = "value"
    ws: weakref.WeakSet[WeakRefDemo] = weakref.WeakSet()
    ws.add(key)
    del key
    gc.collect()
    return len(wkd) == 0, len(ws) == 0


def finalizer_demo() -> list[str]:
    events: list[str] = []

    class Tracked:
        pass

    obj = Tracked()
    weakref.finalize(obj, lambda: events.append("finalized"))
    del obj
    gc.collect()
    return events


def eligible_ineligible_demo() -> tuple[bool, bool]:
    eligible = SlottedWeak("ok")
    ineligible = SlottedNoWeak("no")
    try:
        _ = weakref.ref(eligible)
        ok = True
    except TypeError:
        ok = False
    try:
        _ = weakref.ref(ineligible)
        not_ok = False
    except TypeError:
        not_ok = True
    return ok, not_ok


def callback_cannot_recover_demo() -> tuple[bool, str]:
    recovered: list[Any] = []

    def callback(wr: weakref.ReferenceType[Any]) -> None:
        # Callback receives dead weakref; wr() is None, cannot resurrect.
        recovered.append(wr())

    obj = WeakRefDemo("cb")
    ref = weakref.ref(obj, callback)
    _ = ref
    del obj
    gc.collect()
    # recovered should contain None, not the live object.
    if not recovered:
        gc.collect()
    return len(recovered) == 1, str(recovered[0] is None) if recovered else "no-callback"


def cycle_demo() -> bool:
    # Cycle with weakref breaks otherwise.
    class Node:
        def __init__(self, name: str) -> None:
            self.name = name
            self.next: Node | None = None

    a = Node("a")
    b = Node("b")
    a.next = b
    b.next = a
    ref_a = weakref.ref(a)
    del a, b
    gc.collect()
    return ref_a() is None


def resurrection_note() -> str:
    # __del__ resurrection is not relied upon; we demonstrate non-timing check.
    return "finalizer-cannot-resurrect-checked-via-ref-is-none"
