//! RS-CAN-FFI-002 — export names, sections, link identities.

/// Renamed exported symbol. The Rust name is `renamed_export`; the linker
/// name is `fixture_exported_renamed` (valid fixture exports under a stable
/// renamed identity).
#[unsafe(export_name = "fixture_exported_renamed")]
pub extern "C" fn renamed_export(x: i32) -> i32 {
    x.wrapping_add(100)
}

// Imported renamed symbol from the `ffi_provider` crate. The provider
// exports `fixture_imported_renamed`; this declaration imports it under the
// local name `renamed_import`.
unsafe extern "C" {
    #[link_name = "fixture_imported_renamed"]
    fn renamed_import(x: i32) -> i32;
}

/// Sectioned static placed in a custom linker section. `#[used]` prevents
/// the compiler from eliminating it as dead code; `link_section` creates a
/// linker identity distinct from the Rust path.
#[unsafe(link_section = ".fixture_notes")]
#[used]
pub static SECTIONED_VALUE: u32 = 0xDEADBEEF;

/// Second sectioned static with explicit `no_mangle` to keep its symbol
/// deterministically named for cross-crate linking, also placed in the same
/// fixture section.
#[unsafe(link_section = ".fixture_notes")]
#[used]
#[unsafe(no_mangle)]
pub static SECTIONED_MARKER: u8 = 0x55;

/// Call the renamed imported symbol.
pub fn call_renamed_import(value: i32) -> i32 {
    // SAFETY: `renamed_import` is provided by `ffi_provider` and is valid for
    // arbitrary `i32` values.
    unsafe { renamed_import(value) }
}

/// Direct call to the renamed exported symbol via its Rust name (inside the
/// same crate) and reference to its linker name.
pub fn renamed_export_call_via_rust(value: i32) -> i32 {
    renamed_export(value)
}

/// Expose the sectioned value's address to keep the section alive and to
/// demonstrate that sectioned statics have a stable address.
pub fn sectioned_value() -> u32 {
    SECTIONED_VALUE
}

/// Reference the marker to prevent dead elimination in release profiles.
pub fn sectioned_marker_addr() -> *const u8 {
    core::ptr::addr_of!(SECTIONED_MARKER)
}

/// Marker that the build-script emitted native link directives are present.
/// The cfg `ffi_build_linked` is set by `build.rs` emitting
/// `cargo:rustc-cfg=ffi_build_linked`.
pub fn build_link_marker() -> bool {
    cfg!(ffi_build_linked)
}
