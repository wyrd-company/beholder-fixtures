"""Layered settings resolver fixture package."""

from layered_settings_resolver.class_namespace import (
    PreparedNamespaceMeta,
    SettingsProfile,
    TypeScopedRegistry,
)
from layered_settings_resolver.closure_capture import (
    factory_capture,
    loop_late_binding,
    qualified_locals_name,
)
from layered_settings_resolver.comprehension_scope import (
    class_body_lookup_failure,
    comprehension_forms,
    forbidden_walrus_in_iterable,
    generator_laziness,
    walrus_in_comprehension,
)
from layered_settings_resolver.declarations import (
    missing_nonlocal_reads_enclosing,
    mutate_without_declaration,
    parameter_shadows_enclosing,
    rebind_enclosing,
    rebind_module_global,
)
from layered_settings_resolver.deletion import (
    delete_attribute,
    delete_captured_cell,
    delete_global_name,
    delete_item,
    delete_local_name,
    delete_nonlocal_name,
)
from layered_settings_resolver.exception_targets import (
    exception_group_subgroup,
    handler_target_lifetime,
    retained_traceback_reference,
)
from layered_settings_resolver.explicit_namespaces import (
    closure_exec_support,
    eval_in_mappings,
    exec_in_mappings,
    function_locals_snapshot,
    untrusted_mapping_guard,
)
from layered_settings_resolver.introspection import (
    closure_cells,
    code_object_names,
    frame_locals_snapshot,
    globals_locals_vars,
)
from layered_settings_resolver.leg_lookup import (
    builtin_shadowing,
    class_scope_not_enclosing,
    compile_time_local_classification,
    compile_time_unbound_local_probe,
    read_four_levels,
)
from layered_settings_resolver.name_mangling import (
    ManglingBase,
    ManglingDerived,
    convention_underscores,
    reflection_bypass,
)
from layered_settings_resolver.pattern_binding import (
    guard_side_effects,
    irrefutable_capture,
    qualified_value_pattern,
    unreachable_or_branch,
    wildcard_no_bind,
)

__all__ = [
    "PreparedNamespaceMeta",
    "SettingsProfile",
    "TypeScopedRegistry",
    "builtin_shadowing",
    "class_scope_not_enclosing",
    "closure_cells",
    "closure_exec_support",
    "code_object_names",
    "compile_time_local_classification",
    "comprehension_forms",
    "convention_underscores",
    "delete_attribute",
    "delete_captured_cell",
    "delete_global_name",
    "delete_item",
    "delete_local_name",
    "delete_nonlocal_name",
    "eval_in_mappings",
    "exception_group_subgroup",
    "exec_in_mappings",
    "factory_capture",
    "frame_locals_snapshot",
    "function_locals_snapshot",
    "generator_laziness",
    "globals_locals_vars",
    "guard_side_effects",
    "handler_target_lifetime",
    "irrefutable_capture",
    "loop_late_binding",
    "mutate_without_declaration",
    "qualified_locals_name",
    "qualified_value_pattern",
    "read_four_levels",
    "rebind_enclosing",
    "rebind_module_global",
    "reflection_bypass",
    "retained_traceback_reference",
    "untrusted_mapping_guard",
    "walrus_in_comprehension",
    "wildcard_no_bind",
    "ManglingBase",
    "ManglingDerived",
]
