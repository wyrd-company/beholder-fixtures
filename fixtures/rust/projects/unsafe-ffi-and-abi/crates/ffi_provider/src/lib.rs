//! Rust-defined C-ABI symbols linked across local crate boundaries.

/// C-ABI function provided for RS-CAN-FFI-001 foreign declaration.
#[unsafe(no_mangle)]
pub extern "C" fn fixture_add(a: i32, b: i32) -> i32 {
    a.wrapping_add(b)
}

/// C-ABI static provided for RS-CAN-FFI-001 foreign static.
#[unsafe(no_mangle)]
pub static FIXTURE_COUNTER: i32 = 42;

/// Symbol exported under a renamed linker name for RS-CAN-FFI-002.
/// The Rust item name is `fixture_renamed_source`; the linker sees
/// `fixture_imported_renamed`.
#[unsafe(export_name = "fixture_imported_renamed")]
pub extern "C" fn fixture_renamed_source(x: i32) -> i32 {
    x.wrapping_mul(2)
}

/// Sectioned static is defined in the consuming crate, but a second
/// marker static here anchors the provider side of cross-crate linking
/// and keeps the crate non-trivial for offline builds.
#[unsafe(no_mangle)]
pub static PROVIDER_MARKER: u8 = 0xAA;
