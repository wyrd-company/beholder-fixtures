//! RS-CAN-TYPE-005 — primitive, tuple, array, slice, string, never types.

#[allow(clippy::let_unit_value)]
pub fn tuple_forms() {
    let unit: () = ();
    let _ = unit;

    let one: (u32,) = (42,);
    assert_eq!(one.0, 42);

    let pair: (i32, &str) = (7, "harvest");
    let (a, b) = pair;
    let _ = (a, b);

    // Nested and sized tuples.
    let triple: (u8, u16, u32) = (1, 2, 3);
    assert_eq!(triple.2, 3);
}

pub fn array_and_slice_coercion() {
    const LEN: usize = 4;
    let arr: [i32; LEN] = [1, 2, 3, 4];
    let slice: &[i32] = &arr;
    assert_eq!(slice.len(), LEN);

    // Const-length generic helper.
    assert_eq!(array_sum(arr), 10);

    let borrowed: &[i32] = &arr;
    let _ = borrowed;

    // Mut slice coercion.
    let mut mutable = [10, 20, 30];
    let as_slice: &mut [i32] = &mut mutable;
    as_slice[0] = 99;
    assert_eq!(mutable[0], 99);
}

fn array_sum<const N: usize>(arr: [i32; N]) -> i32 {
    let mut sum = 0;
    for v in arr {
        sum += v;
    }
    sum
}

pub fn string_and_byte_forms() {
    let owned: String = "meadow".to_string();
    let borrowed: &str = &owned;
    assert!(borrowed.contains("mead"));

    // String literal coercion &String -> &str via Deref is covered in coercions
    // but shown here as basic forms.
    let literal: &str = "plot";

    // Byte forms.
    let bytes: &[u8] = b"field";
    assert_eq!(bytes.len(), 5);

    let byte_string: Vec<u8> = b"harvest".to_vec();
    assert_eq!(byte_string[0], b'h');

    // Raw string.
    let raw: &str = r#"path \ without \ escape"#;
    let _ = (literal, raw, bytes);
}

pub fn diverges() -> ! {
    panic!("diverging function for never type")
}

pub fn diverging_branch(is_ready: bool) -> i32 {
    // Diverging branch coerces to any concrete type.
    if is_ready { 42 } else { diverges() }
}

#[allow(clippy::unnecessary_literal_unwrap)]
pub fn never_in_closure() {
    // Never coerces at valid sites, such as match arms and closures.
    let value: i32 = match Some(5) {
        Some(n) => n,
        None => diverges(),
    };
    let _ = value;

    let maybe: Option<i32> = None;
    let _ = maybe.unwrap_or_else(|| diverges());
}

pub fn invalid_by_value_positions_doc() {
    // Invalid by-value DST positions such as `let x: str;` are documented as
    // counterexamples and not compiled here.
    let _ = "valid str is always behind a pointer";
}
