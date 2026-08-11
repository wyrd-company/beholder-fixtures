//! RS-CAN-FFI-005 — inline/global assembly and target-feature calls.

#[cfg(target_arch = "x86_64")]
use core::arch::asm;

/// Target-gated inline assembly with operands and `sym` reference.
/// Only compiled on `x86_64`; other targets see a fallback stub.
#[cfg(target_arch = "x86_64")]
pub fn asm_with_operands(value: u64) -> u64 {
    let out: u64;
    // SAFETY: `asm!` is unsafe by definition. The template uses `mov` to copy
    // the input register to the output, which is valid on x86_64 and has no
    // observable side effects beyond the declared operands.
    unsafe {
        asm!(
            "mov {0}, {1}",
            out(reg) out,
            in(reg) value,
            options(nostack, pure, nomem),
        );
    }
    out
}

#[cfg(not(target_arch = "x86_64"))]
pub fn asm_with_operands(value: u64) -> u64 {
    value
}

/// Demonstrates `asm!` with a `sym` operand referencing a Rust function.
#[cfg(target_arch = "x86_64")]
pub fn asm_with_sym(value: i32) -> i32 {
    // `sym` requires a function with a stable address; we reference `helper_for_sym`.
    unsafe {
        asm!(
            "call {}",
            sym helper_for_sym,
            in("edi") value,
            out("eax") _,
            clobber_abi("C"),
        );
        value.wrapping_add(1)
    }
}

#[cfg(not(target_arch = "x86_64"))]
pub fn asm_with_sym(value: i32) -> i32 {
    helper_for_sym(value)
}

extern "C" fn helper_for_sym(x: i32) -> i32 {
    x.wrapping_add(1)
}

// Global assembly defining a symbol with target-gated `x86_64` code.
// On `x86_64` this declares a global symbol `fixture_global_asm_marker`
// whose address can be taken; on other targets the module is empty and the
// marker symbol is provided as a Rust static instead.
#[cfg(target_arch = "x86_64")]
core::arch::global_asm!(
    ".global fixture_global_asm_marker",
    "fixture_global_asm_marker: ret",
    options(att_syntax),
);

#[cfg(target_arch = "x86_64")]
unsafe extern "C" {
    fn fixture_global_asm_marker();
}

#[cfg(not(target_arch = "x86_64"))]
#[unsafe(no_mangle)]
pub static fixture_global_asm_marker: u8 = 0;

#[cfg(target_arch = "x86_64")]
pub fn global_asm_addr() -> *const () {
    fixture_global_asm_marker as *const ()
}

#[cfg(not(target_arch = "x86_64"))]
pub fn global_asm_addr() -> *const () {
    core::ptr::addr_of!(fixture_global_asm_marker) as *const ()
}

/// Function annotated with `target_feature`. The caller must ensure the
/// feature is present either via compile-time flags or runtime detection.
///
/// # Safety
/// Caller must ensure `sse2` is available on the current CPU (via
/// compile-time target or runtime detection with `is_x86_feature_detected!`).
#[cfg(target_arch = "x86_64")]
#[target_feature(enable = "sse2")]
unsafe fn sse2_target_feature_fn(a: u64, b: u64) -> u64 {
    // Inside SSE2-enabled region we may use an intrinsic. `_mm_pause` is an
    // SSE2 intrinsic that hints to the CPU that we are in a spin loop.
    core::arch::x86_64::_mm_pause();
    a.wrapping_add(b)
}

/// Public wrapper that calls the `target_feature` function only when the
/// target is `x86_64`; on other targets it returns a plain fallback.
pub fn target_feature_demo() -> u64 {
    #[cfg(target_arch = "x86_64")]
    {
        // SAFETY: `x86_64` baseline includes SSE2, so the feature is always
        // present on the declared build target `x86_64-unknown-linux-gnu`.
        unsafe { sse2_target_feature_fn(10, 32) }
    }
    #[cfg(not(target_arch = "x86_64"))]
    {
        42
    }
}

/// Runtime feature detection before using an x86_64 intrinsic.
/// On `x86_64` the detection probes for `sse2` at runtime, then calls the
/// target-feature function and a direct intrinsic behind the same gate;
/// a fallback is used when the feature is absent.
pub fn intrinsic_with_runtime_detection(a: u64, b: u64) -> u64 {
    #[cfg(target_arch = "x86_64")]
    {
        if std::is_x86_feature_detected!("sse2") {
            // SAFETY: `sse2` was detected at runtime. `_mm_pause` is an
            // SSE2 intrinsic valid behind this gate; `sse2_target_feature_fn`
            // is also `#[target_feature(enable = "sse2")]` and therefore
            // requires the same runtime guarantee.
            unsafe {
                core::arch::x86_64::_mm_pause();
                sse2_target_feature_fn(a, b)
            }
        } else {
            a.wrapping_add(b)
        }
    }
    #[cfg(not(target_arch = "x86_64"))]
    {
        let _ = (a, b);
        0
    }
}

/// Small helper that exercises the full asm surface: operands, `sym`, global
/// asm address, intrinsic behind detection, and target-feature call.
pub fn asm_demo() -> u64 {
    let a = asm_with_operands(7);
    let b = asm_with_sym(3) as u64;
    let _addr = global_asm_addr();
    let c = target_feature_demo();
    let d = intrinsic_with_runtime_detection(2, 3);
    a.wrapping_add(b).wrapping_add(c).wrapping_add(d)
}
