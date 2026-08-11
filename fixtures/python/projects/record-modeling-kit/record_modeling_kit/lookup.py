"""Instance, class, and metaclass lookup (PY-CAN-OBJ-005)."""

from __future__ import annotations


class _MetaSharedDesc:
    """Non-data descriptor for metaclass; class dict wins, bare class falls through."""

    def __get__(self, instance: object | None, owner: type | None = None) -> str:
        if instance is None:
            return "from-metaclass"
        return "from-metaclass"


class LookupMeta(type):
    """Metaclass that exposes a descriptor."""

    shared = _MetaSharedDesc()

    @property  # type: ignore[misc]
    def meta_value(self) -> str:  # type: ignore[no-redef]
        return "from-metaclass"


class DataDesc:
    """Data descriptor (has __set__) has priority over instance dict."""

    def __get__(self, instance: object | None, owner: type | None = None) -> str:
        if instance is None:
            return "data-desc-class"
        return "data-desc-instance"

    def __set__(self, instance: object, value: str) -> None:
        instance.__dict__["_data_desc_store"] = f"stored:{value}"


class NonDataDesc:
    """Non-data descriptor (no __set__) loses to instance dict."""

    def __get__(self, instance: object | None, owner: type | None = None) -> str:
        if instance is None:
            return "nondata-desc-class"
        return "nondata-desc-instance"


class LookupBase(metaclass=LookupMeta):
    value = "from-class"
    data_item = DataDesc()
    nondata_item = NonDataDesc()

    # Place Same-named values at each level.
    shared = "from-class-shared"


class DerivedLookup(LookupBase):
    shared = "from-derived"


class InstanceLookupDemo(DerivedLookup):
    def __init__(self) -> None:
        # Instance attribute shadows class attribute unless data descriptor.
        self.shared = "from-instance"
        self.__dict__["nondata_item"] = "instance-nondata"
        self.__dict__["data_item"] = "instance-data-ignored"


class MetaclassLookupDemo(LookupBase):
    pass


class BareMetaLookup(metaclass=LookupMeta):
    """No class-level shared; lookup falls through to metaclass descriptor."""

    pass


def data_vs_nondata_demo() -> tuple[str, str]:
    obj = InstanceLookupDemo()
    # Data descriptor wins over instance dict entry.
    data = obj.data_item
    # Non-data descriptor loses to instance dict entry.
    nondata = obj.nondata_item
    return data, nondata  # type: ignore[return-value]


def metaclass_descriptor_demo() -> str:
    # Metaclass descriptor accessed via class lacking its own attribute.
    return BareMetaLookup.shared  # type: ignore[attr-defined]


def class_assignment_replacement_demo() -> tuple[str, str]:
    class ReplaceDemo(LookupBase):
        tag = "before"

    before = ReplaceDemo.tag
    ReplaceDemo.tag = "after"
    after = ReplaceDemo.tag
    return before, after


def special_lookup_bypass_demo() -> tuple[bool, str]:
    """__len__ special lookup bypasses instance dict."""
    class Special:
        def __len__(self) -> int:
            return 7

    obj = Special()
    # Monkey patch instance dict; len() still uses type.
    obj.__dict__["__len__"] = lambda: 99  # type: ignore[attr-defined]
    via_len = len(obj)
    via_attr = obj.__dict__["__len__"]()  # explicit dict access
    return via_len == 7, f"via_len={via_len} via_attr={via_attr}"


def instance_class_metaclass_resolution_demo() -> tuple[str, str, str]:
    obj = InstanceLookupDemo()
    instance_val = obj.shared  # from instance
    del obj.shared
    class_val = obj.shared  # from class DerivedLookup/LookupBase
    meta_val = BareMetaLookup.shared  # type: ignore[attr-defined]  # from metaclass via same name
    return instance_val, class_val, meta_val  # type: ignore[return-value]


def same_named_triple_demo() -> tuple[str, str, str]:
    """One name shared at instance, class, and metaclass levels."""
    obj = InstanceLookupDemo()
    inst = obj.shared
    cls = LookupBase.shared
    meta = BareMetaLookup.shared  # type: ignore[attr-defined]
    return inst, cls, meta  # type: ignore[return-value]
