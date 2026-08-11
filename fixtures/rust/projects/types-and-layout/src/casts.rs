//! RS-CAN-TYPE-016 — the closed set of `as` casts and library conversions.

use std::convert::{TryFrom, TryInto};

pub fn numeric_casts() {
    // Widening.
    let small: u8 = 200;
    let wide: u16 = small as u16;
    assert_eq!(wide, 200);

    // Truncating.
    let large: u16 = 0x1234;
    let truncated: u8 = large as u8;
    assert_eq!(truncated, 0x34);

    // Float to int truncates toward zero and saturates out-of-range (current Rust).
    let float_val: f64 = 3.9;
    let as_int: i32 = float_val as i32;
    assert_eq!(as_int, 3);

    let huge: f64 = 1e30;
    let saturated: i32 = huge as i32;
    // Out-of-range saturates to T::MAX/MIN rather than wrapping.
    assert_eq!(saturated, i32::MAX);

    let negative_huge: f64 = -1e30;
    let saturated_neg: i32 = negative_huge as i32;
    assert_eq!(saturated_neg, i32::MIN);
}

pub fn enum_and_pointer_casts() {
    #[repr(u8)]
    #[allow(dead_code)]
    enum Level {
        Low = 1,
        Mid = 5,
        High = 20,
    }
    let _ = Level::Low as u8;
    let _ = Level::High as u8;

    // Enum-to-integer cast (fieldless only).
    let level = Level::Mid as u8;
    assert_eq!(level, 5);

    // Pointer casts: raw/fat/thin.
    let value: u32 = 123;
    let const_ptr: *const u32 = &value as *const u32;
    let as_usize: usize = const_ptr as usize;
    let back: *const u32 = as_usize as *const u32;
    assert_eq!(unsafe { *back }, 123);

    // Function pointer cast to raw address.
    fn target(x: i32) -> i32 {
        x + 1
    }
    let fn_ptr: fn(i32) -> i32 = target;
    let as_addr: usize = fn_ptr as usize;
    assert!(as_addr != 0);

    // Fat pointer to thin pointer loses metadata.
    let slice: &[u8] = b"harvest";
    let fat: *const [u8] = slice as *const [u8];
    let thin: *const u8 = fat as *const u8;
    let recovered_len = slice.len();
    let _ = (thin, recovered_len);

    // Thin to fat via slice_from_raw_parts requires length.
    let len = slice.len();
    let rebuilt: *const [u8] = std::ptr::slice_from_raw_parts(thin, len);
    assert_eq!(unsafe { &*rebuilt }, slice);
}

pub fn address_exposure_and_provenance() {
    let value = 99_i32;
    let ptr: *const i32 = &value;
    // Address exposure via cast retains provenance via original pointer abstraction.
    let exposed: usize = ptr as usize;
    let _ = exposed;
    assert_eq!(unsafe { *ptr }, 99);
}

pub fn library_conversions_contrast() {
    // `as` is not general conversion; library traits are preferred.
    let from_val: String = String::from("field");
    #[allow(clippy::useless_conversion)]
    let into_val: String = "meadow".to_string().into();
    assert_eq!(from_val.len(), 5);
    assert_eq!(into_val.len(), 6);

    // Fallible conversion.
    let large: u32 = 300;
    let tried: Result<u8, _> = u8::try_from(large);
    assert!(tried.is_err());

    let small: u32 = 7;
    let ok: u8 = small.try_into().unwrap();
    assert_eq!(ok, 7);

    // `transmute` is not `as`; included only as contrast (no actual call).
    // Correct conversion uses `From` rather than reinterpretation.
}

pub fn cast_coverage_probe() {
    numeric_casts();
    enum_and_pointer_casts();
    address_exposure_and_provenance();
    library_conversions_contrast();
}
