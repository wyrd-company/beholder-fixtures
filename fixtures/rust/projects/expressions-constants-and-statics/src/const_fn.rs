//! RS-CAN-CONST-002 — Const functions and evaluation in many contexts.

/// Stable const fn: only operations that are stable const-evaluable are used.
pub const fn double(value: usize) -> usize {
    value * 2
}

pub const fn add(a: usize, b: usize) -> usize {
    a + b
}

pub const fn checked_add_safe(a: usize, b: usize) -> usize {
    // Only the taken branch must be const-valid; untaken panic path is allowed as long as not evaluated.
    if b == 0 { a } else { a + b }
}

pub const fn select(flag: bool, a: usize, b: usize) -> usize {
    if flag { a } else { b }
}

// Use in array length.
pub const LEN: usize = double(4);
pub const ARRAY: [u8; LEN] = [0; LEN];

// Use in discriminant.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum Choice {
    Alpha = double(1) as u8,
    Beta = double(2) as u8,
    Gamma = 9,
}

// Use in static.
pub static STATIC_FROM_CONST: usize = double(6);

// Use in const-generic.
pub struct Buffer<const N: usize> {
    pub data: [u8; N],
}

pub type SmallBuffer = Buffer<{ double(3) }>;
pub type SelectedBuffer = Buffer<{ select(true, 4, 8) }>;

// Use in runtime context (called at runtime, same body).
pub fn runtime_double(value: usize) -> usize {
    double(value)
}

// Inline-const context.
pub fn inline_const_demo() -> usize {
    (const { double(5) }) + (const { add(2, 3) })
}

// Array length via const fn call.
pub fn array_len_demo() -> usize {
    let _arr: [i32; double(4)] = [1; double(4)];
    _arr.len()
}

// Const-generic function.
pub fn generic_const_usage() -> usize {
    let buf = SmallBuffer {
        data: [0; double(3)],
    };
    let buf2 = SelectedBuffer {
        data: [1; select(true, 4, 8)],
    };
    buf.data.len() + buf2.data.len()
}

// Permit untaken branch: the panic branch is const-valid only if taken, but since we check the condition,
// untaken panic is allowed in const eval (the function itself remains const).
pub const fn maybe_panic(flag: bool) -> usize {
    if flag {
        // This would panic in const if evaluated; but the call site avoids it.
        panic!("const panic when flag true")
    } else {
        10
    }
}

pub const MAYBE_OK: usize = maybe_panic(false);

// Demonstrates generic const fn that could fail after instantiation - not evaluated for invalid input.
pub const fn generic_checked<T>(value: usize) -> usize
where
    T: Sized,
{
    // Simple generic const fn; the failure mode is instantiation-dependent (overflow etc).
    double(value)
}

pub const GENERIC_U32: usize = generic_checked::<u32>(3);

pub fn demonstrate() -> i32 {
    let _ = ARRAY.len();
    let _ = Choice::Alpha as u8;
    let _ = STATIC_FROM_CONST;
    let _ = SmallBuffer {
        data: [0; double(3)],
    }
    .data
    .len();
    let _ = runtime_double(7);
    let _ = inline_const_demo();
    let _ = array_len_demo();
    let _ = generic_const_usage();
    let _ = MAYBE_OK;
    let _ = GENERIC_U32;
    let _ = checked_add_safe(5, 2);
    let _ = select(false, 1, 2);
    1
}
