//! Fixture native sys crate for RS-CAN-PROJ-020 and RS-CAN-ECO-004.
//! Owns `links = "fixture_native"` and compiles hermetic native translation unit.

/// Safe wrapper around vendored `fixture_add`.
pub fn add(a: i32, b: i32) -> i32 {
    unsafe { fixture_add(a, b) }
}

/// Safe wrapper around vendored `fixture_mul`.
pub fn mul(a: i32, b: i32) -> i32 {
    unsafe { fixture_mul(a, b) }
}

unsafe extern "C" {
    fn fixture_add(a: i32, b: i32) -> i32;
    fn fixture_mul(a: i32, b: i32) -> i32;
}

/// Value exported for dependent crates to verify linkage.
pub const NATIVE_KIND: &str = "native";
