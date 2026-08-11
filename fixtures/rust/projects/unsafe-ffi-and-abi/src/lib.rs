//! Fixture for Rust unsafe, FFI, ABI, and runtime contracts.
//! Covers RS-CAN-UNSAFE-001..004, RS-CAN-FFI-001..005, RS-CAN-PROJ-017.

pub mod asm_target;
pub mod ffi_decls;
pub mod ffi_linking;
pub mod ffi_types;
pub mod maybe_uninit;
pub mod no_std_illustration;
pub mod provenance;
pub mod transmute;
pub mod unsafe_ops;
pub mod unwind_boundary;
pub mod wasm_runtime;

pub use ffi_alloc as alloc_crate;
pub use ffi_no_std as no_std_crate;
pub use ffi_provider as provider;

/// Aggregated entry touching each fixture area so that `cargo build` and
/// `cargo clippy` observe reachable valid code.
pub fn fixture_overview() -> &'static str {
    // UNSAFE-001
    let _ = unsafe_ops::raw_dereference_demo();
    let _ = unsafe_ops::unsafe_call_demo(3);
    let _ = unsafe_ops::static_mut_demo();
    let _ = unsafe_ops::union_read_demo();
    let _ = unsafe_ops::safe_wrapper_demo();

    // UNSAFE-002
    let _ = maybe_uninit::staged_value();
    let _ = maybe_uninit::staged_array();

    // UNSAFE-003
    provenance::provenance_demo();
    provenance::in_allocation_demo();
    provenance::one_past_demo();
    provenance::pointer_mapping_demo();

    // UNSAFE-004
    let _ = transmute::transparent_transmute_demo();

    // FFI-001
    let _ = ffi_decls::call_imported();
    let _ = ffi_decls::exported_add(2, 3);
    ffi_decls::variadic_declaration_marker();

    // FFI-002
    let _ = ffi_linking::call_renamed_import(4);
    let _ = ffi_linking::renamed_export(5);
    let _ = ffi_linking::sectioned_value();

    // FFI-003
    let _ = ffi_types::ffi_types_demo();
    let _ = ffi_types::callback_demo();

    // FFI-004
    let _ = unwind_boundary::boundary_demo(false);
    let _ = unwind_boundary::abort_profile_marker();

    // FFI-005
    let _ = asm_target::asm_demo();
    let _ = asm_target::target_feature_demo();

    // PROJ-017
    let _ = no_std_illustration::core_vs_std_option();
    let _ = no_std_illustration::alloc_variant_demo();
    let _ = no_std_illustration::no_std_checksum();

    // wasm hooks are target-gated; reference the module to keep it linked
    // on wasm builds without forcing host inclusion of panic handler.
    let _ = wasm_runtime::wasm_entry_name();

    "unsafe-ffi-and-abi"
}
