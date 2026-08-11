//! Fixture for build-script protocol and code generation.
//! Covers RS-CAN-PROJ-011, RS-CAN-PROJ-012, RS-CAN-PROJ-020, RS-CAN-ECO-004.

use fixture_native_sys as native_sys;

// RS-CAN-PROJ-020: verify DEP_* metadata not available as ordinary env at compile time.
// This is the expected behavior; see docs/counterexamples.md.
// `option_env!` returns None for DEP variables outside build scripts.
const DEP_NOT_IN_ENV: Option<&str> = option_env!("DEP_FIXTURE_NATIVE_FIXTURE_KIND");

// RS-CAN-PROJ-011: use cfg and env emitted by build script.
#[cfg(fixture_build_cfg)]
pub fn fixture_build_cfg_active() -> bool {
    true
}

#[cfg(not(fixture_build_cfg))]
pub fn fixture_build_cfg_active() -> bool {
    false
}

#[cfg(host_target_match)]
pub const HOST_TARGET_MATCH: bool = true;

#[cfg(not(host_target_match))]
pub const HOST_TARGET_MATCH: bool = false;

pub fn build_env_value() -> &'static str {
    env!("FIXTURE_BUILD_ENV")
}

pub fn host_probe() -> (&'static str, &'static str) {
    (env!("FIXTURE_HOST"), env!("FIXTURE_TARGET"))
}

pub fn conditional_value() -> &'static str {
    env!("FIXTURE_CONDITIONAL_VALUE")
}

pub fn consumed_native_present() -> &'static str {
    env!("CONSUMED_NATIVE_PRESENT")
}

// RS-CAN-PROJ-011 + RS-CAN-PROJ-020: build metadata consumption in build.rs
// propagates via DEP_* to consuming build script; ordinary crate sees only
// the derived env `CONSUMED_NATIVE_KIND` when the build script forwarded it.
pub fn consumed_native_kind() -> Option<&'static str> {
    option_env!("CONSUMED_NATIVE_KIND")
}

// RS-CAN-PROJ-012: Rust generated into OUT_DIR and included as items.
pub mod generated_items {
    include!(concat!(env!("OUT_DIR"), "/generated_items.rs"));
}

pub mod generated_expr {
    pub fn expr_value() -> u32 {
        // Item and expression inclusion via include! in expression position.
        include!(concat!(env!("OUT_DIR"), "/generated_expression.rs"))
    }
}

// RS-CAN-PROJ-012: separate embedded text and bytes constants.
pub const EMBEDDED_TEXT: &str = include_str!(concat!(env!("OUT_DIR"), "/generated_text.txt"));
pub const EMBEDDED_BYTES: &[u8] = include_bytes!(concat!(env!("OUT_DIR"), "/generated_bytes.bin"));

// RS-CAN-PROJ-012: relative and OUT_DIR include paths.
pub mod relative_via_include {
    // Relative path (relative to this file's directory).
    include!("included_relative.rs");
}

pub mod out_dir_via_include {
    // OUT_DIR absolute path via concat!(env!("OUT_DIR"), ...)
    include!(concat!(env!("OUT_DIR"), "/generated_items.rs"));
}

// RS-CAN-PROJ-012: one file both included and module-mounted.
// Handwritten file `dual_source.rs` is mounted as a module and also included
// via `include!`, producing distinct entities.

#[path = "dual_source.rs"]
pub mod dual_mounted;

pub mod dual_included {
    include!("dual_source.rs");
}

// Additional demonstration: generated dual file included in two ways.
pub mod generated_dual_included {
    include!(concat!(env!("OUT_DIR"), "/dual.rs"));
}

pub mod generated_dual_again {
    include!(concat!(env!("OUT_DIR"), "/dual.rs"));
}

// RS-CAN-ECO-004: hermetic native translation unit exposed via safe wrapper.
pub fn native_add(a: i32, b: i32) -> i32 {
    native_sys::add(a, b)
}

pub fn native_mul(a: i32, b: i32) -> i32 {
    native_sys::mul(a, b)
}

pub fn native_kind() -> &'static str {
    native_sys::NATIVE_KIND
}

// Verify that distinct includes produce distinct types.
pub fn demonstrate_distinct_types() {
    // `dual_mounted::DualType` and `dual_included::DualType` are distinct nominal types
    // despite identical textual source; assignment between them fails to compile.
    let a = dual_mounted::DualType(1);
    let b = dual_included::DualType(2);
    // Use both to avoid unused warnings.
    assert_eq!(a.value(), 1);
    assert_eq!(b.value(), 2);

    // Similarly, generated dual includes produce distinct types.
    let c = generated_dual_included::DualType(3);
    let d = generated_dual_again::DualType(4);
    assert_eq!(c.value(), 3);
    assert_eq!(d.value(), 4);
}

// Ensure dep metadata counterexample is observable.
pub fn dep_metadata_in_build_script_only() -> Option<&'static str> {
    DEP_NOT_IN_ENV
}
