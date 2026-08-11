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


resurrected_store: list[Any] = []


class Resurrectable:
    def __del__(self) -> None:
        # Resurrection: re-anchor self in global store.
        resurrected_store.append(self)


def resurrection_demo() -> tuple[bool, bool]:
    resurrected_store.clear()
    obj = Resurrectable()
    ref = weakref.ref(obj)
    del obj
    gc.collect()
    # Non-timing check: object was resurrected via __del__ (store non-empty) even though original ref cleared.
    was_resurrected = len(resurrected_store) == 1
    still_alive_via_store = resurrected_store[0] is not None if was_resurrected else False
    # Clean up resurrected reference for future runs.
    resurrected_store.clear()
    gc.collect()
    return was_resurrected, still_alive_via_store


def finalizer_shutdown_demo() -> tuple[bool, bool]:
    events: list[str] = []
    obj = WeakRefDemo("shutdown")
    fin = weakref.finalize(obj, lambda: events.append("finalized"))
    # Explicitly configure shutdown behavior: finalize at interpreter exit vs immediate.
    fin.atexit = False
    atexit_false = fin.atexit is False
    fin.atexit = True
    atexit_true = fin.atexit is True
    # Trigger immediate finalization via deletion (non-timing).
    del obj
    gc.collect()
    was_finalized = len(events) == 1
    return atexit_true and atexit_false, was_finalized


def resurrection_note() -> tuple[bool, bool]:
    # Backward alias for coverage; delegates to resurrection_demo.
    return resurrection_demo()
