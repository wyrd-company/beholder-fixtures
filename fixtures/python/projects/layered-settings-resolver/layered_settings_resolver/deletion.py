"""Deletion and absent bindings (PY-CAN-BIND-010)."""

from __future__ import annotations

from types import MappingProxyType


class DescriptorSlot:
    """Descriptor whose deletion path is explicit."""

    def __init__(self) -> None:
        self._value: str | None = "present"

    def __get__(self, instance, owner) -> str | None:
        return self._value

    def __delete__(self, instance) -> None:
        self._value = None


class SettingsBag:
    slot = DescriptorSlot()

    def __init__(self) -> None:
        self.values: dict[str, int] = {"mode": 1}


def delete_local_name() -> None:
    """Delete a local binding and observe `UnboundLocalError` on reuse."""

    token = "local"
    del token


def delete_global_name() -> None:
    """Delete a module-global name."""

    global _DELETE_ME
    _DELETE_ME = "temporary"
    del _DELETE_ME


_DELETE_ME: str | None = None


def delete_nonlocal_name() -> int:
    """Delete a `nonlocal` binding inside a nested function."""

    counter = 2

    def reset() -> int:
        nonlocal counter
        del counter
        counter = 5
        return counter

    return reset()


def delete_attribute(target: SettingsBag) -> None:
    """Delete an instance attribute."""

    target.label = "tenant"
    del target.label


def delete_item(target: SettingsBag) -> None:
    """Delete a mapping item."""

    del target.values["mode"]


def delete_captured_cell() -> str:
    """Delete a name captured by a nested function cell."""

    label = "layer"

    def reader() -> str:
        return label

    snapshot = reader()
    del label
    return snapshot


def repeated_deletion(proxy: MappingProxyType) -> bool:
    """Show repeated deletion is not applicable to read-only views."""

    return len(proxy) >= 0
