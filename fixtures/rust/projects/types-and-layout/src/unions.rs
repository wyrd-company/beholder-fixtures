//! RS-CAN-TYPE-003 — unions with `Copy` and `ManuallyDrop` fields.

use std::mem::ManuallyDrop;

// Overlapping `Copy` fields.
#[derive(Clone, Copy)]
pub union CopyUnion {
    pub as_u32: u32,
    pub as_i32: i32,
    pub as_bytes: [u8; 4],
}

// Union containing a `ManuallyDrop` field; drop fields would be rejected.
pub union DropUnion {
    pub number: i32,
    pub text: ManuallyDrop<String>,
}

// FFI-compatible union.
#[repr(C)]
pub union CUnion {
    pub small: u16,
    pub large: u32,
}

pub fn safe_writes() {
    // Writes to union fields are safe.
    let mut u = CopyUnion { as_u32: 0 };
    u.as_i32 = -7;
    let _observed = unsafe { u.as_i32 };
    u.as_u32 = 42;
    let _ = unsafe { u.as_u32 };

    let mut with_drop = DropUnion { number: 10 };
    with_drop.number = 20;
    with_drop.text = ManuallyDrop::new("harvest".to_string());

    // Clean up ManuallyDrop content manually.
    unsafe {
        ManuallyDrop::drop(&mut with_drop.text);
    }
}

pub fn unsafe_reads() -> (i32, String) {
    let u = CopyUnion { as_i32: -5 };
    let a = unsafe { u.as_i32 };
    let b = unsafe { u.as_u32 } as i32;

    let mut holder = DropUnion {
        text: ManuallyDrop::new("meadow".to_string()),
    };
    let cloned = unsafe { (*holder.text).clone() };
    // Safety: we keep the allocation alive through `holder` and then drop it.
    unsafe {
        ManuallyDrop::drop(&mut holder.text);
    }
    (a + b, cloned)
}

pub fn c_union_example() -> u32 {
    let u = CUnion { large: 0x1234_5678 };
    unsafe { u.large }
}

pub fn pattern_restriction_note() {
    // Union pattern restrictions and invalid bit patterns are documented in
    // `docs/counterexamples.md`; valid usage goes through field access.
    let _ = CopyUnion { as_u32: 1 };
}
