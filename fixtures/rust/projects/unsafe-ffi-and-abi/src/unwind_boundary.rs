//! RS-CAN-FFI-004 — unwinding across ABI boundaries.

use core::ffi::c_void;

/// `extern "C"` callback (non-unwinding ABI). Unwinding across this boundary
/// is undefined behavior and is never executed in the valid fixture.
extern "C" fn c_callback(value: i32) -> i32 {
    value.wrapping_add(1)
}

/// `extern "C-unwind"` callback that is allowed to unwind.
extern "C-unwind" fn unwind_callback(value: i32) -> i32 {
    if value < 0 {
        panic!("unwind_callback: negative value {value}");
    }
    value.wrapping_mul(2)
}

/// C-ABI function that takes an `extern "C"` callback. The valid path does
/// not unwind through it.
pub fn call_c_boundary(callback: extern "C" fn(i32) -> i32, value: i32) -> i32 {
    callback(value)
}

/// C-ABI function that takes an `extern "C-unwind"` callback. The caller is
/// responsible for catching any unwind at the boundary.
pub fn call_unwind_boundary(callback: extern "C-unwind" fn(i32) -> i32, value: i32) -> i32 {
    callback(value)
}

/// `extern "C" fn` that uses `catch_unwind` at the boundary. This is the
/// correct pattern for `C-unwind` boundaries that need to handle Rust panics.
pub extern "C" fn c_boundary_with_catch(value: i32) -> i32 {
    std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| unwind_callback(value))).unwrap_or(-1)
}

/// Demonstrates the boundary without unwinding (valid fixture path).
pub fn boundary_demo(should_panic: bool) -> i32 {
    // Non-unwind path via `extern "C"` stays successful.
    let a = call_c_boundary(c_callback, 10);

    // `C-unwind` path with catch at the boundary.
    let b = if should_panic {
        c_boundary_with_catch(-5)
    } else {
        call_unwind_boundary(unwind_callback, 10)
    };

    // `catch_unwind` variant that returns a `Result`, mirroring the common
    // FFI boundary pattern where the foreign caller checks for -1 sentinel.
    let c =
        std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| unwind_callback(3))).unwrap_or(-1);

    // Keep `c_void` context variant visible as well (callback with context).
    let _ctx_ptr = core::ptr::null_mut::<c_void>();

    a + b + c
}

/// Marker that the crate builds under both panic strategies. With
/// `panic = "abort"` (profile `abort`), `catch_unwind` still compiles but the
/// panic never unwinds; the runtime aborts instead. The valid fixture never
/// triggers a panic in that profile.
pub fn abort_profile_marker() -> &'static str {
    if cfg!(panic = "abort") {
        "abort"
    } else {
        "unwind"
    }
}
