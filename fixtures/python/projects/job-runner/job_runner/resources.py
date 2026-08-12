"""Resource lifetime and garbage collection (PY-CAN-FLOW-008)."""

from __future__ import annotations

import gc
import weakref


class ManagedResource:
    """Context manager whose close is prompt via with, delayed via deletion."""

    def __init__(self, name: str, log: list[str]) -> None:
        self.name = name
        self.log = log
        self.closed = False

    def __enter__(self) -> ManagedResource:
        self.log.append(f"enter-{self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.close()
        return False

    def close(self) -> None:
        if not self.closed:
            self.closed = True
            self.log.append(f"close-{self.name}")

    def __del__(self) -> None:
        # __del__ may run late, during GC, or not at all if cycle involves it.
        # Globals may be None at shutdown.
        try:
            self.close()
        except Exception:
            pass


def with_vs_deletion() -> list[str]:
    """with guarantees prompt close; del merely drops a name and relies on refcount."""
    log: list[str] = []

    # Prompt close via with
    with ManagedResource("with-job", log):
        log.append("inside-with")

    # Deletion of name — CPython refcount closes promptly, other impls may delay
    res = ManagedResource("del-job", log)
    log.append("before-del")
    del res
    # Under CPython, close already happened; explicitly collect to cover cycle case
    gc.collect()
    log.append("after-del")
    return log


class CycleMember:
    """Participate in reference cycle to show gc effect."""

    def __init__(self, name: str, log: list[str]) -> None:
        self.name = name
        self.log = log
        self.peer: CycleMember | None = None

    def __del__(self) -> None:
        try:
            self.log.append(f"del-{self.name}")
        except Exception:
            pass


def reference_cycle_and_collection() -> list[str]:
    """Create a cycle and show collection requires gc."""
    log: list[str] = []
    a = CycleMember("a", log)
    b = CycleMember("b", log)
    a.peer = b
    b.peer = a
    # Break cycle explicitly vs relying on collector
    del a
    del b
    collected = gc.collect()
    log.append(f"collected-{collected}")
    return log


class CyclicFinalizer:
    """Cycle with __del__ demonstrates unpredictable finalization order."""

    def __init__(self, name: str, log: list[str]) -> None:
        self.name = name
        self.log = log
        self.ref: CyclicFinalizer | None = None

    def __del__(self) -> None:
        # Resurrection and shutdown-globals caveats
        try:
            self.log.append(f"finalize-{self.name}")
            # Resurrection: store self somewhere would resurrect, but we avoid
            # keeping reference to demonstrate.
            if self.name == "resurrect":
                # Do not actually resurrect in fixture; just note the possibility.
                pass
        except Exception:
            pass


def cyclic_finalization_order() -> list[str]:
    """Cyclic objects with __del__ need gc and order is unspecified."""
    log: list[str] = []
    gc.disable()
    try:
        x = CyclicFinalizer("x", log)
        y = CyclicFinalizer("y", log)
        x.ref = y
        y.ref = x
        del x
        del y
        gc.collect()
        log.append("after-collect")
    finally:
        gc.enable()
    return log


def weak_finalizer() -> list[str]:
    """weakref.finalize runs callback when referent is reclaimed without resurrection."""
    log: list[str] = []

    class JobHandle:
        pass

    handle = JobHandle()
    weakref.finalize(handle, lambda: log.append("finalizer-ran"))
    # Also demonstrate weakref callback
    ref = weakref.ref(handle, lambda r: log.append("weakref-callback"))
    del handle
    gc.collect()
    log.append(f"ref-dead-{ref() is None}")
    return log


_resurrected: list[object] = []


class ResurrectingJob:
    """Valid resurrection variant: __del__ retains self without timing assertion."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __del__(self) -> None:
        try:
            _resurrected.append(self)
        except Exception:
            pass


def resurrection_variant() -> dict[str, object]:
    """Retain self during finalization and release without asserting timing."""
    _resurrected.clear()
    job = ResurrectingJob("resurrected-job")
    job_id = id(job)
    del job
    gc.collect()
    resurrected_now = len(_resurrected) == 1 and id(_resurrected[0]) == job_id
    # Release without asserting collection order or exact timing
    _resurrected.clear()
    gc.collect()
    return {"resurrected": resurrected_now, "released": len(_resurrected) == 0}


def resurrection_note() -> str:
    """Resurrection inside __del__ keeps object alive one more cycle."""

    # If __del__ stores self globally, the object is resurrected and __del__
    # will not be called again until resurrected reference dies. CPython
    # handles this; other implementations may differ.
    return "resurrection-keeps-object-alive-until-next-collection"


def shutdown_globals_note() -> str:
    """At interpreter shutdown globals may be None, so __del__ must guard."""
    return "shutdown-globals-may-be-None-guard-__del__"


def prompt_refcount_vs_delayed_gc_note() -> str:
    """CPython refcount reclaims promptly; other impls may delay until gc."""
    return "cpython-prompt-refcount-vs-delayed-gc-unspecified-timing"
