//! RS-CAN-EXPR-009 — Literals, suffixes, escapes, and fallback.

/// Numeric bases, separators, and suffixes.
pub fn numeric_variants() -> i64 {
    let decimal: i32 = 42;
    let with_separators: i32 = 1_000_000;
    let binary: u8 = 0b1010_1010;
    let octal: u16 = 0o755;
    let hex_lower: u32 = 0xdead_beef;
    let hex_upper: u32 = 0xDEAD_BEEF;
    let suffixed_u8: u8 = 255_u8;
    let suffixed_i64: i64 = 9_999_i64;
    let suffixed_usize: usize = 12_usize;
    let unsuffixed_inferred: i32 = 7;
    let float_default: f64 = 3.14;
    let float_suffixed: f32 = 2.5_f32;
    let float_scientific: f64 = 1.5e10;
    let float_separator: f64 = 1_000.5;

    // Inferred numerics via target type.
    let inferred_vec: Vec<i32> = vec![1, 2, 3];
    let _ = inferred_vec;

    // Boundary: negative literal is parsed as unary negation of positive literal.
    let negative_boundary: i32 = -128;
    let _ = negative_boundary;

    decimal as i64
        + with_separators as i64
        + suffixed_i64
        + suffixed_usize as i64
        + unsuffixed_inferred as i64
        + binary as i64
        + octal as i64
        + hex_lower as i64
        + hex_upper as i64
        + suffixed_u8 as i64
        + float_default as i64
        + float_suffixed as i64
        + float_scientific as i64
        + float_separator as i64
}

/// Inferred numerics demonstration: suffix not required when type context exists.
pub fn inferred_variants() -> (i32, u64) {
    let inferred_int = 42;
    let explicit: i32 = inferred_int;
    let inferred_float = 2.0;
    let explicit_f: f64 = inferred_float;
    // Turbofish inference.
    let parsed: i32 = "7".parse::<i32>().unwrap_or(0);
    let collected: Vec<u64> = vec![1_u64, 2, 3];
    (
        explicit + parsed,
        collected.len() as u64 + explicit_f as u64,
    )
}

/// String and char literal variants.
pub fn string_and_char_variants() -> usize {
    let ch_ascii: char = 'a';
    let ch_unicode: char = 'µ';
    let ch_escape: char = '\n';
    let ch_unicode_escape: char = '\u{03B1}';
    let byte_char: u8 = b'a';
    let byte_escape: u8 = b'\n';

    let str_simple: &str = "harvest";
    let str_escape: &str = "line\nbreak\t tab \"quote\" 'single' \\backslash \0null";
    let str_unicode: &str = "µ α \u{03B2} \u{1F33E}";
    let byte_str: &[u8] = b"bytes \x41 \n";
    let raw_str: &str = r#"raw "quotes" \no escape"#;
    let raw_str_hashes: &str = r##"raw with hash"##;
    let raw_str_count: &str = r###"raw with many"###;
    let raw_byte_str: &[u8] = br"raw bytes";
    let raw_byte_hashes: &[u8] = br##"raw bytes two"##;

    // C-string literal (stable since 1.77) producing `&CStr`.
    let c_str: &std::ffi::CStr = c"harvest";
    let c_str_with_escape: &std::ffi::CStr = c"plot";
    let _ = c_str_with_escape;

    ch_ascii.len_utf8()
        + ch_unicode.len_utf8()
        + ch_escape.len_utf8()
        + ch_unicode_escape.len_utf8()
        + byte_char as usize
        + byte_escape as usize
        + str_simple.len()
        + str_escape.len()
        + str_unicode.len()
        + byte_str.len()
        + raw_str.len()
        + raw_str_hashes.len()
        + raw_str_count.len()
        + raw_byte_str.len()
        + raw_byte_hashes.len()
        + c_str.count_bytes()
}

pub fn demonstrate() -> i32 {
    let _ = numeric_variants();
    let _ = inferred_variants();
    let _ = string_and_char_variants();
    1
}
