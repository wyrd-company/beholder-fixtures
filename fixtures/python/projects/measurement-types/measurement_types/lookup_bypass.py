"""Special-method lookup bypass (PY-CAN-PROT-010)."""

from __future__ import annotations


class InstanceSpecial:
    """Type defines ``__len__``; instance attribute does not affect syntax."""

    def __len__(self) -> int:
        return 5


class PatchedLen:
    """Empty type whose ``__len__`` is added later by patching the type."""

    pass


class MetaWithCall(type):
    """Metaclass with ``__call__`` influencing class construction."""

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance.metaclass_constructed = True
        return instance


class ConstructedViaMeta(metaclass=MetaWithCall):
    """Class whose construction path goes through metaclass ``__call__``."""

    def __init__(self) -> None:
        self.metaclass_constructed = False


def instance_special_bypass_demo() -> tuple[int, int, bool]:
    """Contrast explicit instance attribute access versus syntactic lookup."""

    obj = InstanceSpecial()
    # Attach a per-instance callable that looks like ``__len__``
    obj.__len__ = lambda: 99  # type: ignore[attr-defined]
    syntactic = len(obj)  # ignores instance attribute, uses type
    explicit = obj.__len__()  # explicit attribute access
    same = syntactic == explicit
    return syntactic, explicit, same


def type_patch_affects_existing_demo() -> tuple[int, int]:
    """Patching the type after instantiation affects existing instances."""

    obj = PatchedLen()
    before = "present" if hasattr(type(obj), "__len__") else "absent"
    # Patch the type
    PatchedLen.__len__ = lambda self: 42  # type: ignore[attr-defined]
    after = len(obj)
    # Cleanup: remove for isolation
    del PatchedLen.__len__  # type: ignore[attr-defined]
    return (0 if before == "absent" else 1), after


def operation_specific_paths_demo() -> tuple[int, str]:
    """Show that ``len`` uses ``__len__`` while addition uses ``__add__``."""

    class Dual:
        def __len__(self) -> int:
            return 7

        def __add__(self, other: object) -> str:
            return "added"

    obj = Dual()
    length = len(obj)
    added = obj + object()  # type: ignore[operator]
    return length, added


def metaclass_case_demo() -> bool:
    """Construct via metaclass ``__call__`` and verify the flag."""

    obj = ConstructedViaMeta()
    return bool(getattr(obj, "metaclass_constructed", False))
