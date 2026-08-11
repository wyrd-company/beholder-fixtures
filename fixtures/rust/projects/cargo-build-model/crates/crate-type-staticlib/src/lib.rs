//! RS-CAN-PROJ-014: staticlib crate type (C-ABI static library).

#[unsafe(no_mangle)]
pub extern "C" fn staticlib_exported_fn() -> u32 {
    4
}

pub fn rust_fn() -> u32 {
    44
}
