//! RS-CAN-PROJ-017 freestanding runtime hooks, target-gated on `wasm32-unknown-unknown`.
//!
//! The wasm32 freestanding variant provides the entry symbol, panic handler,
//! and global allocator that a `no_std` Wasm module requires. The actual
//! definitions live in `crates/ffi_wasm_runtime` (no_std, wasm-gated) so the
//! host `std` build remains free of duplicate lang items.

/// Name of the Wasm entry symbol provided when targeting `wasm32-unknown-unknown`.
pub fn wasm_entry_name() -> &'static str {
    if cfg!(target_arch = "wasm32") {
        "_start"
    } else {
        "host"
    }
}
