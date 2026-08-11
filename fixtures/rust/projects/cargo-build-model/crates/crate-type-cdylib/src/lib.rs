//! RS-CAN-PROJ-014: cdylib crate type (C-ABI dynamic library).
//! Contrast Rust `pub` API with exported C-ABI symbols.

#[unsafe(no_mangle)]
pub extern "C" fn cdylib_exported_fn() -> u32 {
    3
}

pub fn rust_pub_fn() -> u32 {
    33
}

// Internal Rust API not exported via C ABI.
pub struct CdylibType(pub u32);
