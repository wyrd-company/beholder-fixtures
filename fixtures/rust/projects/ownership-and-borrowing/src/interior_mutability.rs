//! RS-CAN-OWN-005: Interior mutability.

use std::cell::{Cell, RefCell, UnsafeCell};

/// Cell demo: interior mutation through shared reference.
pub fn cell_demo() -> i32 {
    let c = Cell::new(5);
    c.set(10);
    let v = c.get();
    c.replace(20);
    v + c.get()
}

/// RefCell successful shared and mutable borrows.
pub fn refcell_success() -> i32 {
    let rc = RefCell::new(10);
    {
        let b1 = rc.borrow();
        let b2 = rc.borrow();
        let _ = *b1 + *b2;
    }
    {
        let mut m = rc.borrow_mut();
        *m += 5;
    }
    *rc.borrow()
}

/// RefCell detection of conflicting borrow without panicking the process.
/// `try_borrow_mut` returns `Err` when a shared borrow is live; the panicking
/// `borrow_mut` path is documented in `docs/counterexamples.md`.
pub fn refcell_try_conflict() -> bool {
    let rc = RefCell::new(1);
    let _shared = rc.borrow();
    rc.try_borrow_mut().is_err()
}

/// RefCell panicking borrow caught via `catch_unwind` so the fixture remains valid.
pub fn refcell_panicking_caught() -> bool {
    let rc = RefCell::new(2);
    let result = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
        let _b = rc.borrow();
        // This would panic: `borrow_mut` while `borrow` is live.
        let _m = rc.borrow_mut();
    }));
    result.is_err()
}

/// Minimal sound `UnsafeCell` abstraction.
/// Provides interior mutability behind `&self` with a safe API restricted to
/// `Copy` get/set so no live reference can be re-entered. This prevents safe
/// reentrant aliasing through callbacks that capture the same cell.
/// Safety: `UnsafeCell` is the only source of aliasing; the safe API never
/// hands out a reference that could overlap mutation, so aliasing rules are
/// preserved. The wrapper is `!Sync` by containing `UnsafeCell`.
pub struct SoundCell<T> {
    inner: UnsafeCell<T>,
}

impl<T> SoundCell<T> {
    pub fn new(value: T) -> Self {
        Self {
            inner: UnsafeCell::new(value),
        }
    }

    pub fn set(&self, value: T) {
        unsafe {
            *self.inner.get() = value;
        }
    }

    pub fn get(&self) -> T
    where
        T: Copy,
    {
        unsafe { *self.inner.get() }
    }
}

// SoundCell is !Sync due to UnsafeCell; we do not impl Sync.

/// Demonstrate SoundCell usage.
pub fn sound_cell_demo() -> i32 {
    let c = SoundCell::new(100);
    c.set(200);
    let v = c.get();
    c.set(v + 1);
    let w = c.get();
    v + w - 200
}

pub fn interior_mutability_summary() -> (i32, i32, bool, bool, i32) {
    let a = cell_demo();
    let b = refcell_success();
    let c = refcell_try_conflict();
    let d = refcell_panicking_caught();
    let e = sound_cell_demo();
    (a, b, c, d, e)
}
