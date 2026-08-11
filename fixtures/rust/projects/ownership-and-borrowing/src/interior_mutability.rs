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
/// Provides interior mutability behind `&self` with a safe API.
/// Safety: single-threaded access; no creation of aliasing mutable references
/// that overlap with live shared references outside the abstraction boundary.
/// This wrapper is `!Sync` by containing `UnsafeCell`.
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

    pub fn with<R>(&self, f: impl FnOnce(&T) -> R) -> R {
        unsafe { f(&*self.inner.get()) }
    }

    pub fn with_mut<R>(&self, f: impl FnOnce(&mut T) -> R) -> R {
        unsafe { f(&mut *self.inner.get()) }
    }
}

// SoundCell is !Sync due to UnsafeCell; we do not impl Sync.

/// Demonstrate SoundCell usage.
pub fn sound_cell_demo() -> i32 {
    let c = SoundCell::new(100);
    c.set(200);
    let v = c.get();
    c.with_mut(|x| *x += 1);
    let w = c.with(|x| *x);
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
