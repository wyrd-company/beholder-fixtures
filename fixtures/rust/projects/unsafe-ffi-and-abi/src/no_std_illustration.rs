//! RS-CAN-PROJ-017 — no_std, alloc, and core vs std identity.

/// Identical core type through `std` and `core` paths.
/// Both spellings name the same type when `std` is available.
pub fn core_vs_std_option() -> bool {
    let via_core: core::option::Option<u32> = Some(7);
    let via_std: std::option::Option<u32> = Some(7);
    via_core == via_std
}

/// Demonstrates that `core::fmt`, `std::fmt`, and `alloc::fmt` describe the
/// same traits when `std` is present, while `core` remains valid under
/// `no_std`.
pub fn core_vs_std_fmt(value: u32) -> String {
    use core::fmt::Write as _;
    let mut buf = String::new();
    let _ = core::write!(&mut buf, "{value}");
    buf
}

/// no_std library usage on the host target.
/// The `ffi_no_std` crate is `#![no_std]` and compiles on the host via the
/// workspace's host build; its API is exercised here without requiring
/// `std` in that crate itself.
pub fn no_std_checksum() -> u32 {
    let rec = ffi_no_std::Record::new(11, false);
    ffi_no_std::checksum(&rec)
}

/// alloc-using variant on the host target.
/// `ffi_alloc` is `#![no_std]` with `extern crate alloc`; building the
/// workspace on the host compiles this crate with its `alloc` dependency.
pub fn alloc_variant_demo() -> usize {
    let ids = [1u32, 2, 3, 4];
    let records = ffi_alloc::alloc_vec_example(&ids);
    let sum = ffi_alloc::alloc_checksum(&records);
    let _label = ffi_alloc::alloc_record_label(&records[0]);
    assert!(sum > 0);
    records.len()
}

/// Alloc example that proves `Vec`/`String` construction via `alloc` rather
/// than `std` directly, while still being callable from a `std` context.
pub fn alloc_string_demo() -> String {
    ffi_alloc::alloc_record_label(&ffi_no_std::Record::new(99, true))
}
