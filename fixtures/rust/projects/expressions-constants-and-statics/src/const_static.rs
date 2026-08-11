//! RS-CAN-CONST-001 — Constants, inline const, and statics.

use std::sync::atomic::AtomicUsize;

/// Free constants.
pub const FREE_A: i32 = 42;
pub const FREE_B: &str = "harvest";

/// Associated constants.
pub struct Orchard;

impl Orchard {
    pub const ROWS: usize = 8;
    pub const LABEL: &'static str = "plot";
}

/// Generic inline const context: captures generic parameter via inline const.
pub fn generic_inline_const<T>(value: T) -> usize
where
    T: std::fmt::Debug,
{
    // Inline const that captures `T`-related value from the generic context.
    (const { std::mem::size_of::<usize>() })
        + {
            // This inline const uses the generic param's associated constant size.
            let _ = const { std::mem::size_of::<T>() };
            0
        }
        + {
            // Capture value's discriminant length via formatting length (runtime), combined with const eval.
            let _ = format!("{value:?}");
            1
        }
}

/// Unnamed constant used to trigger compile-time assertion: `_` pattern const.
const _: () = assert!(FREE_A == 42);
const _: () = assert!(Orchard::ROWS > 0);
const ASSERT_CONST: () = assert!(FREE_B.len() == 7);

/// Immutable static.
pub static IMMUTABLE: i32 = 100;

/// Interior-mutable static (Sync via interior mutability).
pub static INTERIOR_MUTABLE: AtomicUsize = AtomicUsize::new(0);
pub static SHARED_COUNTER: AtomicUsize = AtomicUsize::new(0);

/// Mutable static: access is unsafe (edition 2024 denies creating safe reference to `static mut`).
pub static mut MUTABLE_STATIC: i32 = 0;

/// Demonstrates immutable, interior-mutable, and mutable statics.
pub fn static_demonstrations() -> i32 {
    // Immutable static has one storage location; taking address observes stable identity.
    let addr1: *const i32 = &IMMUTABLE;
    let addr2: *const i32 = &IMMUTABLE;
    assert_eq!(addr1, addr2);

    // Const is inlined: two uses produce equal values but not necessarily same address.
    let const_addr1: *const i32 = &FREE_A;
    let const_addr2: *const i32 = &FREE_A;
    // Addresses may or may not be equal (const has no stable address identity); just ensure value read works.
    assert_eq!(unsafe { *const_addr1 }, 42);
    assert_eq!(unsafe { *const_addr2 }, 42);

    // Interior-mutable static via atomic.
    INTERIOR_MUTABLE.store(5, std::sync::atomic::Ordering::SeqCst);
    let prev = INTERIOR_MUTABLE.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
    assert_eq!(prev, 5);

    SHARED_COUNTER.fetch_add(2, std::sync::atomic::Ordering::SeqCst);

    // Mutable static requires unsafe to access; edition 2024 denies shared ref to static mut.
    unsafe {
        MUTABLE_STATIC = 7;
        MUTABLE_STATIC += 1;
        let val = std::ptr::addr_of!(MUTABLE_STATIC).read();
        assert_eq!(val, 8);
        let raw: *mut i32 = std::ptr::addr_of_mut!(MUTABLE_STATIC);
        *raw = 9;
        assert_eq!(*raw, 9);
    }

    // Inline const with generic capture.
    let _ = generic_inline_const::<i32>(5);
    let _ = generic_inline_const::<String>(String::from("row"));

    // Inline const block demonstrating that it creates a const-evaluation context.
    let inline_val: i32 = const { FREE_A + 8 };
    let _generic_inline: usize = const { std::mem::size_of::<usize>() + Orchard::ROWS };

    assert_eq!(ASSERT_CONST, ());

    inline_val
}

/// Compile-time assertion helper to confirm const evaluation.
pub const fn is_positive(value: i32) -> bool {
    value > 0
}

const CHECK_POSITIVE: () = assert!(is_positive(FREE_A));

pub fn demonstrate() -> i32 {
    let _ = CHECK_POSITIVE;
    static_demonstrations()
}
