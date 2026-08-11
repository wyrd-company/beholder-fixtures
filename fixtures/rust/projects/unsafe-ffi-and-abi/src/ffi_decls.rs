//! RS-CAN-FFI-001 — foreign blocks, functions, statics, ABI strings.

// Imported C-ABI function and static from the local `ffi_provider` crate.
// Edition 2024 requires `unsafe extern`. The imported symbols are
// Rust-defined C-ABI symbols linked across local crate boundaries.
unsafe extern "C" {
    fn fixture_add(a: i32, b: i32) -> i32;
    static FIXTURE_COUNTER: i32;
}

// Safe-qualified foreign import where the callee guarantees safety for all
// inputs. Demonstrates the `safe extern "C"` form alongside `unsafe extern`.
#[allow(clashing_extern_declarations)]
unsafe extern "C" {
    #[link_name = "fixture_add"]
    safe fn safe_fixture_add(a: i32, b: i32) -> i32;
}

// Variadic foreign declaration (imported). The declaration itself is valid
// fixture source; calling it with variadic arguments requires matching
// the provided foreign definition's calling convention.
unsafe extern "C" {
    fn fixture_variadic_placeholder(count: i32, ...) -> i32;
}

/// Call the imported C-ABI function.
pub fn call_imported() -> i32 {
    // SAFETY: `fixture_add` is provided by the linked `ffi_provider` crate and
    // is valid to call with arbitrary `i32` values.
    unsafe { fixture_add(10, 32) }
}

/// Call the safe-qualified import without an outer unsafe block.
/// The function itself is declared `safe`, so the call site is safe even
/// though the foreign block is `unsafe extern`.
pub fn call_safe_imported() -> i32 {
    safe_fixture_add(3, 4)
}

/// Read the imported C-ABI static.
pub fn read_imported_static() -> i32 {
    // SAFETY: `FIXTURE_COUNTER` is a Rust-defined immutable static exposed
    // with C linkage; reading it is safe under Rust's static safety rules.
    unsafe { FIXTURE_COUNTER }
}

/// C-exported function defined in this crate. Uses `extern "C"` ABI and
/// `#[unsafe(no_mangle)]` so the symbol is visible to foreign consumers.
#[unsafe(no_mangle)]
pub extern "C" fn exported_add(a: i32, b: i32) -> i32 {
    a.wrapping_add(b)
}

/// C-exported static with visible symbol.
#[unsafe(no_mangle)]
pub static EXPORTED_VALUE: i32 = 0x1234;

/// Marker that the variadic declaration exists as valid fixture source.
/// The valid fixture does not execute a UB-inducing mismatched variadic call;
/// any such mismatch is documented in `docs/counterexamples.md`.
pub fn variadic_declaration_marker() -> bool {
    // The declaration `fixture_variadic_placeholder` is present; we avoid
    // calling it with a mismatched signature, which would be UB.
    let _fn_ptr: unsafe extern "C" fn(i32, ...) -> i32 = fixture_variadic_placeholder;
    true
}
