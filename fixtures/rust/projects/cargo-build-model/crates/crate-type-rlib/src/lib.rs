//! RS-CAN-PROJ-014: one compatible library source compiled under the rlib,
//! dylib, cdylib, and staticlib crate-type boundaries. This file is the shared
//! source for all four; `crates/crate-type-dylib`, `crate-type-cdylib`, and
//! `crate-type-staticlib` each declare their own package with `path = "../crate-type-rlib/src/lib.rs"`
//! and a single, distinct `crate-type`, so the exact same source compiles into
//! four different link/export-boundary artifacts.
pub fn rlib_fn() -> u32 {
    1
}
pub struct RlibType(pub u32);

/// C-ABI export boundary, compiled into every crate-type artifact; only the
/// cdylib and staticlib artifacts make it usable from outside Rust.
#[unsafe(no_mangle)]
pub extern "C" fn crate_type_exported_fn() -> u32 {
    100
}
