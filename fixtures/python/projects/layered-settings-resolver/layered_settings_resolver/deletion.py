"""Deletion and absent bindings (PY-CAN-BIND-010)."""

from __future__ import annotations


class DescriptorSlot:
    """Data descriptor whose deletion makes subsequent reads raise.

    Defining ``__delete__`` makes this a data descriptor, so ``__get__`` runs on
    every instance read. After ``__delete__`` clears the presence flag, reads
    raise ``AttributeError``, matching the observed post-``del`` behavior.
    """

    def __init__(self) -> None:
        self._present = True

    def __get__(self, instance, owner) -> "DescriptorSlot | str":
        if instance is None:
            return self
        if not self._present:
            raise AttributeError("slot")
        return "present"

    def __delete__(self, instance) -> None:
        self._present = False


class SettingsBag:
    slot = DescriptorSlot()

    def __init__(self) -> None:
        self.values: dict[str, int] = {"mode": 1}


def delete_local_name() -> str:
    """Delete a local binding and observe `UnboundLocalError` on reuse."""

    token = "local"
    del token
    try:
        _ = token
        return "no-error"
    except UnboundLocalError:
        return "unbound-local"


def delete_global_name() -> str:
    """Delete a module-global name and observe `NameError` on reuse."""

    global _DELETE_ME
    _DELETE_ME = "temporary"
    del _DELETE_ME
    try:
        _ = _DELETE_ME
        return "no-error"
    except NameError:
        return "name-error"


_DELETE_ME: str | None = None


def delete_nonlocal_name() -> tuple[str, int]:
    """Delete a `nonlocal` binding and observe `NameError`, then rebind it.

    A deleted free (cell) variable raises `NameError` on read, not the
    `UnboundLocalError` a deleted fast local raises, so this variant catches
    `NameError` before rebinding the cell.
    """

    counter = 2

    def reset() -> tuple[str, int]:
        nonlocal counter
        del counter
        try:
            _ = counter
            first = "no-error"
        except NameError:
            first = "name-error"
        counter = 5
        return first, counter

    return reset()


def delete_attribute(target: SettingsBag) -> str:
    """Delete an instance attribute and observe `AttributeError` on reuse."""

    target.label = "tenant"
    del target.label
    try:
        _ = target.label
        return "no-error"
    except AttributeError:
        return "attribute-error"


def delete_item(target: SettingsBag) -> str:
    """Delete a mapping item and observe `KeyError` on repeated deletion."""

    del target.values["mode"]
    try:
        del target.values["mode"]
        return "no-error"
    except KeyError:
        return "key-error"


def delete_descriptor(target: SettingsBag) -> str:
    """Delete through a descriptor and observe `AttributeError` on reuse."""

    del target.slot
    try:
        _ = target.slot
        return "no-error"
    except AttributeError:
        return "attribute-error"


def delete_captured_cell() -> str:
    """Delete a captured name before the closure reads it."""

    label = "layer"

    def reader() -> str:
        return label

    del label
    try:
        return reader()
    except NameError:
        return "name-error"


def repeated_deletion(mapping: dict[str, int]) -> str:
    """Observe `KeyError` when deleting the same mapping key twice."""

    del mapping["mode"]
    try:
        del mapping["mode"]
        return "no-error"
    except KeyError:
        return "key-error"
