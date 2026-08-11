"""Cooperative task toolkit of callables, decorators, generators, and async iteration."""

from async_task_toolkit.parameters import (
    builtin_positional_only_contrast,
    duplicate_keyword_failure as param_duplicate_failure,
    missing_required_failure,
    positional_keyword_misuse,
    schedule_task,
    valid_unpacking_variants,
)
from async_task_toolkit.defaults import (
    capture_outer_label,
    collect_with_sentinel,
    collect_with_shared_default,
    default_ordering_rules,
)
from async_task_toolkit.unpacking import (
    custom_mapping_unpacking,
    duplicate_keyword_failure as unpack_duplicate_failure,
    interleaved_unpacking_with_side_effects,
    left_to_right_evaluation,
    non_string_keyword_failure,
)
from async_task_toolkit.first_class import (
    distinct_factory_instances,
    factory,
    lambda_identity,
    named_handler,
    rebinding_leaves_metadata,
    reference_edge_vs_call_edge,
)
from async_task_toolkit.decorators import (
    arbitrary_expression_target,
    replaced_target,
    stacked_handler,
)
from async_task_toolkit.methods import Toolkit, access_through_class_and_instance, raw_class_dictionary
from async_task_toolkit.callable_objects import Parcel, StatefulHandler, use_stateful_callback
from async_task_toolkit.partial_tools import ParcelBatch, bound_method_partial, double, scale_payload
from async_task_toolkit.caching import Shipment, cached_weight, cache_identity_and_state
from async_task_toolkit.generators import (
    explicit_return_value,
    generator_expression_variant,
    parcel_stream,
)
from async_task_toolkit.delegation import capture_subgenerator_return, delegating_generator
from async_task_toolkit.coroutines import CustomAwaitable, parcel_fetch, schedule_and_await
from async_task_toolkit.async_iteration import ParcelAsyncIterator, parcel_async_generator
from async_task_toolkit.context_vars import (
    nested_propagation,
    task_context_capture,
    thread_transition,
    token_reset_order,
)
from async_task_toolkit.metadata import inspect_metadata, parcel_handler, signature_inspection

__all__ = [
    "CustomAwaitable",
    "Parcel",
    "ParcelAsyncIterator",
    "ParcelBatch",
    "Shipment",
    "StatefulHandler",
    "Toolkit",
    "arbitrary_expression_target",
    "bound_method_partial",
    "cache_identity_and_state",
    "cached_weight",
    "capture_subgenerator_return",
    "capture_outer_label",
    "collect_with_sentinel",
    "collect_with_shared_default",
    "custom_mapping_unpacking",
    "default_ordering_rules",
    "delegating_generator",
    "distinct_factory_instances",
    "double",
    "explicit_return_value",
    "factory",
    "generator_expression_variant",
    "inspect_metadata",
    "interleaved_unpacking_with_side_effects",
    "lambda_identity",
    "left_to_right_evaluation",
    "named_handler",
    "nested_propagation",
    "non_string_keyword_failure",
    "parcel_async_generator",
    "parcel_fetch",
    "parcel_handler",
    "parcel_stream",
    "raw_class_dictionary",
    "rebinding_leaves_metadata",
    "reference_edge_vs_call_edge",
    "replaced_target",
    "scale_payload",
    "schedule_and_await",
    "schedule_task",
    "signature_inspection",
    "stacked_handler",
    "task_context_capture",
    "thread_transition",
    "token_reset_order",
    "unpack_duplicate_failure",
    "use_stateful_callback",
    "valid_unpacking_variants",
    "access_through_class_and_instance",
    "builtin_positional_only_contrast",
]
