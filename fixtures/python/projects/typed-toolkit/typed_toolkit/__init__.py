"""Statically typed utility library exercising annotation and typing surface."""

from typed_toolkit.annotation_regimes import (
    InventoryItem,
    raw_annotations_demo,
    resolved_hints_demo,
    stringized_raw_check,
)
from typed_toolkit.variable_declarations import Record, module_label
from typed_toolkit.generic_aliases import modern_aliases, get_args_demo
from typed_toolkit.type_aliases import SimpleAlias, InventoryId as AliasInventoryId
from typed_toolkit.type_params import Pep695Box, WithDefault
from typed_toolkit.generics import NewBox, OldBox
from typed_toolkit.protocols import Labelled, Closeable
from typed_toolkit.callable_types import apply_twice, preserving_decorator
from typed_toolkit.overloads import process, runtime_overloads_demo
from typed_toolkit.typed_dicts import InventoryRecord, plain_dict_is_typed_dict
from typed_toolkit.literals import Batch as LiteralBatch, handle_mode
from typed_toolkit.narrowing_predicates import InventoryId, is_inventory_id
from typed_toolkit.self_override import Batch as SelfBatch, ValidOverride
from typed_toolkit.variadic import VariadicBox, specialize_many
from typed_toolkit.stubs_demo import BatchStore
from typed_toolkit.dataclass_transforms import InventoryModel, BatchRecord
from typed_toolkit.annotated_metadata import Batch as AnnotatedBatch, preserve_ordered_metadata_demo
from typed_toolkit.narrowing import exhaustive_status, narrow_via_match
from typed_toolkit.static_imports import create_batch
from typed_toolkit.wrong_annotations import mislabeled

__all__ = [
    "AliasInventoryId",
    "AnnotatedBatch",
    "BatchRecord",
    "BatchStore",
    "Closeable",
    "InventoryId",
    "InventoryItem",
    "InventoryModel",
    "InventoryRecord",
    "Labelled",
    "LiteralBatch",
    "NewBox",
    "OldBox",
    "Pep695Box",
    "Record",
    "SelfBatch",
    "SimpleAlias",
    "ValidOverride",
    "VariadicBox",
    "WithDefault",
    "apply_twice",
    "create_batch",
    "exhaustive_status",
    "get_args_demo",
    "handle_mode",
    "is_inventory_id",
    "mislabeled",
    "modern_aliases",
    "module_label",
    "narrow_via_match",
    "plain_dict_is_typed_dict",
    "preserve_ordered_metadata_demo",
    "preserving_decorator",
    "process",
    "raw_annotations_demo",
    "resolved_hints_demo",
    "runtime_overloads_demo",
    "specialize_many",
    "stringized_raw_check",
]
