//! RS-CAN-UNSAFE-001 — unsafe blocks, functions, traits, and impls.

use core::mem::ManuallyDrop;

/// Mutable static requiring unsafe access.
pub static mut SHARED_COUNTER: i32 = 0;

/// Union whose inactive field read requires unsafe.
#[repr(C)]
pub union DemoUnion {
    pub as_u32: u32,
    pub as_i32: i32,
    pub bytes: [u8; 4],
}

/// Unsafe trait whose implementation asserts a safety contract.
///
/// # Safety
/// Implementors must guarantee that `describe` returns a valid static string
/// and upholds the documented contract of the marker.
pub unsafe trait UnsafeMarker {
    fn describe(&self) -> &'static str;
}

/// Type implementing the unsafe trait behind a safe wrapper.
pub struct Marked(pub i32);

unsafe impl UnsafeMarker for Marked {
    fn describe(&self) -> &'static str {
        "marked"
    }
}

/// Safe wrapper that exposes only safe API despite internally using unsafe.
pub fn safe_wrapper_demo() -> &'static str {
    let value = Marked(7);
    // Safe call through the safe wrapper; the unsafe impl itself is trusted.
    value.describe()
}

/// Unsafe function that dereferences a raw pointer. Must be called inside
/// an explicit `unsafe` block (edition 2024 lint: unsafe_op_in_unsafe_fn).
///
/// # Safety
/// Caller must guarantee both pointers are valid for read for the duration
/// of the call.
pub unsafe fn unsafe_add(a: *const i32, b: *const i32) -> i32 {
    // SAFETY: caller guarantees both pointers are valid for read.
    unsafe { *a + *b }
}

/// Raw pointer dereference inside an unsafe block.
pub fn raw_dereference_demo() -> i32 {
    let value: i32 = 41;
    let ptr: *const i32 = &value as *const i32;
    // SAFETY: `ptr` points at a live stack value for the duration of this block.
    unsafe { *ptr }
}

/// Unsafe call inside an unsafe block.
pub fn unsafe_call_demo(input: i32) -> i32 {
    let other: i32 = 1;
    let a: *const i32 = &input as *const i32;
    let b: *const i32 = &other as *const i32;
    // SAFETY: both `a` and `b` are valid for read.
    unsafe { unsafe_add(a, b) }
}

/// Mutable-static access and update inside unsafe.
pub fn static_mut_demo() -> i32 {
    // SAFETY: single-threaded fixture access; exclusive access is asserted by
    // the caller contract of this demo function.
    unsafe {
        SHARED_COUNTER += 1;
        SHARED_COUNTER
    }
}

/// Union read requires unsafe; writes are safe.
pub fn union_read_demo() -> u32 {
    let mut union_value = DemoUnion { as_u32: 0x01020304 };
    // Safe write.
    union_value.as_u32 = 0x0A0B0C0D;
    // SAFETY: `as_u32` was the last written field, so reading it is valid.
    unsafe { union_value.as_u32 }
}

/// Example that combines raw mut pointer, mutable static, and ManuallyDrop
/// to show the unsafe surface stays explicit.
pub fn combined_unsafe_demo() -> i32 {
    let mut local = 9_i32;
    let raw: *mut i32 = &mut local as *mut i32;
    // SAFETY: `raw` is valid for write for this stack frame.
    unsafe {
        *raw += 1;
        SHARED_COUNTER = *raw;
        SHARED_COUNTER
    }
}

/// Demonstrates that a private inner union read still requires unsafe, even
/// when wrapped in a safe helper that documents the precondition.
pub fn union_byte_view(value: u32) -> [u8; 4] {
    let u = DemoUnion { as_u32: value };
    // SAFETY: `bytes` shares the same storage as `as_u32`; reading the byte
    // representation of a `u32` is valid for any bit pattern.
    unsafe { u.bytes }
}

/// Helper referenced by `fixture_overview` to keep drop semantics visible.
pub fn drop_helper_demo() {
    let _guard = ManuallyDrop::new(Marked(3));
}
