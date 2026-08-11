//! RS-CAN-PROJ-014: crate types overview is re-exported from dedicated crates.
//! This module documents the rlib/dylib/cdylib/staticlib/proc-macro boundaries
//! while the actual linker-facing artifacts are built as separate workspace members.

/// Rust `pub` API vs C-ABI exported symbols: the `crate-type-cdylib` crate exposes
/// `extern "C"` symbols, while `crate-type-rlib` exposes Rust `pub` items with metadata.
pub fn crate_type_boundary_demo() -> &'static str {
    "rlib provides Rust metadata, cdylib provides C-ABI exports"
}
