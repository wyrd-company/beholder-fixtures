"""Record modeling kit fixture package."""

from record_modeling_kit.class_creation import (
    BaseMarker,
    CustomNamespace,
    ReplacementDecoratorDemo,
    evaluated_bases,
    mro_entries_demo,
)
from record_modeling_kit.construction import (
    BypassedInitializer,
    CachedInstance,
    CooperativeChild,
    ForeignResult,
    ImmutablePoint,
)
from record_modeling_kit.mro import (
    DiamondBase,
    DiamondLeft,
    DiamondRight,
    DiamondLeaf,
)
from record_modeling_kit.super_usage import (
    SuperDiamondBase,
    SuperDiamondLeft,
    SuperDiamondRight,
    SuperDiamondLeaf,
)
from record_modeling_kit.lookup import (
    InstanceLookupDemo,
    MetaclassLookupDemo,
)
from record_modeling_kit.descriptors import (
    CachedDescriptor,
    ValidatingDescriptor,
)
from record_modeling_kit.properties import (
    ManagedRecord,
)
from record_modeling_kit.interception import (
    ForwardingProxy,
)
from record_modeling_kit.slots import (
    SlottedBase,
    SlottedWithDict,
    SlottedWithWeakref,
)
from record_modeling_kit.abstract_virtual import (
    DataSink,
    FileSink,
    HookedShape,
)
from record_modeling_kit.init_subclass_hooks import (
    RegisteredModel,
    TaggedDescriptor,
)
from record_modeling_kit.mutation import (
    PatchableService,
)
from record_modeling_kit.dataclasses_kit import (
    BaseItem,
    FrozenItem,
    KwOnlyItem,
    SlottedItem,
)
from record_modeling_kit.enumerations import (
    Color,
    Perm,
    Status,
)
from record_modeling_kit.named_tuples import (
    PointTuple,
    LabeledPoint,
)
from record_modeling_kit.identity import (
    EqualDistinct,
    HashableRecord,
)
from record_modeling_kit.weakrefs import (
    WeakRefDemo,
)
from record_modeling_kit.subscription import (
    SubscribableModel,
)
from record_modeling_kit.custom_checks import (
    DynamicCheckMeta,
)
from record_modeling_kit.dynamic_classes import (
    make_local_class,
    build_dynamic_type,
)

__all__ = [
    "BaseMarker",
    "BypassedInitializer",
    "CachedDescriptor",
    "CachedInstance",
    "Color",
    "CooperativeChild",
    "CustomNamespace",
    "DataSink",
    "DiamondBase",
    "DiamondLeaf",
    "DiamondLeft",
    "DiamondRight",
    "DynamicCheckMeta",
    "EqualDistinct",
    "FileSink",
    "ForeignResult",
    "ForwardingProxy",
    "FrozenItem",
    "BaseItem",
    "HashableRecord",
    "HookedShape",
    "ImmutablePoint",
    "InstanceLookupDemo",
    "KwOnlyItem",
    "LabeledPoint",
    "ManagedRecord",
    "MetaclassLookupDemo",
    "PatchableService",
    "PointTuple",
    "RegisteredModel",
    "ReplacementDecoratorDemo",
    "SlottedBase",
    "SlottedItem",
    "SlottedWithDict",
    "SlottedWithWeakref",
    "Status",
    "Perm",
    "SubscribableModel",
    "SuperDiamondBase",
    "SuperDiamondLeaf",
    "SuperDiamondLeft",
    "SuperDiamondRight",
    "TaggedDescriptor",
    "ValidatingDescriptor",
    "WeakRefDemo",
    "build_dynamic_type",
    "evaluated_bases",
    "make_local_class",
    "mro_entries_demo",
]
