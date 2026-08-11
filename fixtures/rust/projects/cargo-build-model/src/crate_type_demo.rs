//! RS-CAN-PROJ-014: crate types overview is re-exported from dedicated crates.
//! This module documents the rlib/dylib/cdylib/staticlib/proc-macro boundaries
//! while the actual linker-facing artifacts are built as separate workspace members
//! that all compile the one shared source in `crates/crate-type-rlib/src/lib.rs`.

/// Rust `pub` API vs C-ABI exported symbols: every `crate-type-*` package compiles
/// the same source (`rlib_fn`, `RlibType`, and the exported `crate_type_exported_fn`),
/// under a different `[lib] crate-type`, so the artifact boundary differs while the
/// source and its exported symbol do not.
pub fn crate_type_boundary_demo() -> &'static str {
    "one compatible source, four crate-type boundaries (rlib/dylib/cdylib/staticlib)"
}
