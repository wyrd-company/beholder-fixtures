//! RS-CAN-CONST-003 — Static promotion and thread-local storage.

use std::cell::Cell;
use std::sync::atomic::{AtomicUsize, Ordering};

/// Promotable: immutable borrow of a const-evaluable rvalue.
/// The borrow is promoted to hidden static storage, so its address has static duration.
pub fn promotable_borrow() -> &'static i32 {
    // Single promotion site: `&42` is a const-evaluable rvalue borrowed as `&'static i32`
    // and therefore promoted to hidden static storage. The returned reference remains
    // valid for the program's duration and dereferences to 42.
    &42
}

/// Direct promotion observation: static duration without assuming cross-site deduplication.
pub fn promotion_address_stable() -> bool {
    let promoted: &'static i32 = promotable_borrow();
    // Reusing the same promoted reference yields the same address; Rust guarantees
    // static storage duration for this site, not that two distinct `&42` literals
    // from different sites share an address. We verify duration and value, not deduplication.
    let reused = promoted;
    std::ptr::eq(promoted, reused) && *promoted == 42 && *reused == 42
}

/// Non-promotable: interior-mutating borrow (Cell) cannot be promoted to immutable static.
pub fn nonpromotable_interior_mut() -> bool {
    let c: &Cell<i32> = &Cell::new(42);
    // Each call creates a new temporary `Cell`, not promoted.
    let d: &Cell<i32> = &Cell::new(42);
    // Addresses must differ (different temporaries). This demonstrates non-promotion.
    !std::ptr::eq(c as *const _, d as *const _)
}

/// Non-promotable: destructor-bearing value cannot be promoted.
pub struct WithDrop(pub String);

impl Drop for WithDrop {
    fn drop(&mut self) {}
}

pub fn nonpromotable_with_drop() -> bool {
    let a: &WithDrop = &WithDrop(String::from("field"));
    let b: &WithDrop = &WithDrop(String::from("field"));
    !std::ptr::eq(a as *const _, b as *const _)
}

/// Runtime-dependent value that cannot be promoted: depends on function argument.
#[allow(dangling_pointers_from_locals)]
pub fn runtime_dependent_not_promoted(input: i32) -> *const i32 {
    let borrowed: &i32 = &input;
    // This borrow is not promotable because it borrows a runtime value, not a const-evaluable rvalue.
    // Its address is stack-local, not hidden static.
    borrowed as *const i32
}

/// Demonstrates that promotion differs from temporary lifetime extension:
/// a temporary bound inside a block is dropped at block end, not promoted.
pub fn promotion_vs_temporary() -> i32 {
    let value: i32 = {
        let tmp = String::from("temp");
        tmp.len() as i32
    };
    // `tmp` was dropped; no promotion extended its life beyond block.
    value
}

// Stable thread-local storage via `thread_local!` macro.
thread_local! {
    static TLS_COUNTER: Cell<usize> = const { Cell::new(0) };
    static TLS_BUFFER: Cell<usize> = const { Cell::new(0) };
}

static GLOBAL_TLS_FALLBACK: AtomicUsize = AtomicUsize::new(0);

/// Thread-local counter: per-thread identity.
pub fn tls_increment() -> usize {
    TLS_COUNTER.with(|c| {
        let next = c.get() + 1;
        c.set(next);
        next
    })
}

pub fn tls_get() -> usize {
    TLS_COUNTER.with(|c| c.get())
}

pub fn tls_reset() {
    TLS_COUNTER.with(|c| c.set(0));
    TLS_BUFFER.with(|c| c.set(0));
}

/// Demonstrates per-thread identity by spawning a thread and observing its TLS differs.
pub fn tls_per_thread_identity() -> (usize, usize) {
    tls_reset();
    let main_first = tls_increment();
    let main_second = tls_increment();
    assert_eq!(main_first, 1);
    assert_eq!(main_second, 2);

    let handle = std::thread::spawn(|| {
        // New thread starts with its own TLS = 0.
        let child_first = tls_increment();
        let child_second = tls_increment();
        (child_first, child_second)
    });

    let (child_first, child_second) = handle.join().expect("thread joined");
    assert_eq!(child_first, 1);
    assert_eq!(child_second, 2);

    // Main TLS still 2, not affected by child.
    let main_after = tls_get();
    assert_eq!(main_after, 2);

    let _ = GLOBAL_TLS_FALLBACK.fetch_add(1, Ordering::SeqCst);

    (main_after, child_second)
}

pub fn demonstrate() -> i32 {
    let _ = promotable_borrow();
    let _ = promotion_address_stable();
    let _ = nonpromotable_interior_mut();
    let _ = nonpromotable_with_drop();
    let _ = runtime_dependent_not_promoted(99);
    let _ = promotion_vs_temporary();
    let _ = tls_per_thread_identity();
    tls_reset();
    1
}
