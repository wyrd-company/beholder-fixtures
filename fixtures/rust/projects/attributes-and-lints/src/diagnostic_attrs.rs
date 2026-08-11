//! Diagnostic and API-shaping attributes.

use lint_downstream::{ExternalChoice, downstream_score, external_record, legacy_reader};

/// Scoped lint allow on a deprecated call site.
#[allow(deprecated)]
pub fn deprecated_call_site() -> i32 {
    let record = external_record(3);
    legacy_reader(&record)
}

/// Must-use call site demonstrating downstream `must_use` attribute.
pub fn must_use_call_site() -> i32 {
    downstream_score()
}

/// Cross-crate non-exhaustive enum match requiring wildcard arm.
pub fn cross_crate_summary(choice: ExternalChoice) -> &'static str {
    match choice {
        ExternalChoice::Alpha => "alpha",
        ExternalChoice::Beta => "beta",
        _ => "other",
    }
}

/// `track_caller` attribute returning caller location.
#[track_caller]
pub fn track_caller_site() -> &'static std::panic::Location<'static> {
    std::panic::Location::caller()
}

/// Semantic codegen attribute `no_mangle` on a C-ABI exported function.
#[unsafe(no_mangle)]
pub extern "C" fn semantic_exported_symbol() -> i32 {
    11
}

/// Hint codegen attributes `inline` and `cold` on separate items.
#[inline]
pub fn inline_hint_fn() -> i32 {
    1
}

#[cold]
pub fn cold_hint_fn() -> i32 {
    2
}

/// Summary of hint versus semantic codegen attributes.
pub fn codegen_hint_summary() -> &'static str {
    "inline_and_cold_hints"
}

/// Local deprecated item with scoped lint allow at call site.
#[deprecated(note = "use `replacement_value` instead")]
pub fn local_deprecated() -> i32 {
    0
}

/// Local must-use return type.
#[must_use = "record the local score"]
pub fn local_must_use() -> i32 {
    5
}

/// Scoped lint allow suppressing deprecation at the call site.
#[allow(deprecated)]
pub fn use_local_deprecated() -> i32 {
    local_deprecated()
}
