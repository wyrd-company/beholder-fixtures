//! RS-CAN-CONCUR-002 — atomics and memory orderings.
//! Uses `target_has_atomic`-gated width selection on the host.

use std::sync::atomic::{AtomicBool, AtomicI32, AtomicU32, AtomicUsize, Ordering, fence};

#[cfg(target_has_atomic = "64")]
use std::sync::atomic::AtomicU64;

#[cfg(not(target_has_atomic = "64"))]
use std::sync::atomic::AtomicU32 as AtomicU64Compat;

pub fn load_store_demo() {
    let flag = AtomicBool::new(false);
    flag.store(true, Ordering::Release);
    let loaded = flag.load(Ordering::Acquire);
    assert!(loaded);

    let counter = AtomicU32::new(0);
    counter.store(5, Ordering::Relaxed);
    assert_eq!(counter.load(Ordering::Relaxed), 5);
    counter.store(10, Ordering::SeqCst);
    assert_eq!(counter.load(Ordering::SeqCst), 10);
}

pub fn read_modify_write_demo() {
    let value = AtomicU32::new(10);
    let prev = value.fetch_add(5, Ordering::AcqRel);
    assert_eq!(prev, 10);
    assert_eq!(value.load(Ordering::Relaxed), 15);

    let prev_sub = value.fetch_sub(3, Ordering::AcqRel);
    assert_eq!(prev_sub, 15);

    let prev_or = value.fetch_or(0b1000, Ordering::AcqRel);
    assert_eq!(prev_or, 12);
    let prev_and = value.fetch_and(0b0111, Ordering::AcqRel);
    let _ = (prev_and, value.load(Ordering::Relaxed));

    let prev_swap = value.swap(99, Ordering::AcqRel);
    assert_eq!(value.load(Ordering::Relaxed), 99);
    let _ = prev_swap;

    // fetch_update as a read-modify-write variant.
    let current = AtomicI32::new(5);
    let res = current.fetch_update(Ordering::SeqCst, Ordering::SeqCst, |x| Some(x + 1));
    assert!(res.is_ok());
}

pub fn compare_exchange_demo() {
    let cell = AtomicU32::new(0);

    // Strong compare-exchange with valid orderings.
    let ok = cell.compare_exchange(0, 1, Ordering::AcqRel, Ordering::Acquire);
    assert_eq!(ok, Ok(0));
    assert_eq!(cell.load(Ordering::Relaxed), 1);

    let fail = cell.compare_exchange(0, 2, Ordering::SeqCst, Ordering::Relaxed);
    assert_eq!(fail, Err(1));

    // Weak compare-exchange (may spuriously fail).
    let weak = cell.compare_exchange_weak(1, 42, Ordering::SeqCst, Ordering::Relaxed);
    // Weak CAS may succeed or fail spuriously; loop to succeed for deterministic demo.
    if weak.is_err() {
        let _ = cell.compare_exchange(1, 42, Ordering::SeqCst, Ordering::Relaxed);
    }
    // Ensure final state is observable.
    let _ = cell.load(Ordering::SeqCst);
}

pub fn fence_demo() {
    let flag = AtomicBool::new(false);
    let data = AtomicUsize::new(0);

    // Release fence before publishing, acquire fence after observing.
    data.store(123, Ordering::Relaxed);
    fence(Ordering::Release);
    flag.store(true, Ordering::Relaxed);

    fence(Ordering::Acquire);
    let seen = flag.load(Ordering::Relaxed);
    assert!(seen);
    let _ = data.load(Ordering::Relaxed);

    // Compiler fence vs hardware fence distinction documented in counterexamples;
    // `std::sync::atomic::compiler_fence` is also valid but not required here.
    fence(Ordering::SeqCst);
}

#[cfg(target_has_atomic = "64")]
pub fn gated_width_demo() -> u64 {
    let wide = AtomicU64::new(0);
    wide.store(u64::MAX, Ordering::SeqCst);
    wide.fetch_add(1, Ordering::SeqCst);
    wide.load(Ordering::SeqCst)
}

#[cfg(not(target_has_atomic = "64"))]
pub fn gated_width_demo() -> u32 {
    let fallback = AtomicU64Compat::new(0);
    fallback.store(u32::MAX, Ordering::SeqCst);
    fallback.fetch_add(1, Ordering::SeqCst);
    fallback.load(Ordering::SeqCst) as u32
}

pub fn cfg_gated_atomic_demo() {
    // Demonstrate cfg-gated width availability without asserting the flag itself.
    // On x86_64-unknown-linux-gnu, `target_has_atomic = "64"` is true, so the
    // `AtomicU64` branch compiles and executes.
    let value = gated_width_demo();
    // After storing MAX and adding 1, wrapping is intentional via atomic semantics.
    // For u64 MAX + 1 wraps to 0; for u32 fallback the same.
    assert_eq!(value, 0);

    // Also demonstrate cfg-gated selection inline.
    #[cfg(target_has_atomic = "16")]
    {
        use std::sync::atomic::AtomicU16;
        let narrow = AtomicU16::new(0);
        narrow.store(10, Ordering::Relaxed);
        assert_eq!(narrow.load(Ordering::Relaxed), 10);
    }

    #[cfg(not(target_has_atomic = "16"))]
    {
        // Fallback when 16-bit atomics are unavailable (not taken on this host).
        let fallback = AtomicU32::new(0);
        fallback.store(10, Ordering::Relaxed);
        assert_eq!(fallback.load(Ordering::Relaxed), 10);
    }
}

pub fn atomics_demo() {
    load_store_demo();
    read_modify_write_demo();
    compare_exchange_demo();
    fence_demo();
    cfg_gated_atomic_demo();
}
