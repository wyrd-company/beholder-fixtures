//! RS-CAN-TYPE-014 — inference flow, numeric fallback, and target-directed selection.

use std::collections::HashMap;
use std::str::FromStr;

pub fn explicit_and_turbofish() {
    // Explicit annotation selects impl.
    let parsed: i32 = "42".parse().unwrap();
    assert_eq!(parsed, 42);

    // Turbofish selects impl.
    let parsed2 = "7".parse::<u32>().unwrap();
    assert_eq!(parsed2, 7_u32);

    // Inferred target selects impl.
    let target: Vec<i32> = vec![1, 2, 3];
    let collected: Vec<String> = target.into_iter().map(|n| n.to_string()).collect();
    assert_eq!(collected.len(), 3);

    // Inferred collection target.
    let values = ["plot", "meadow"];
    let joined: String = values.join("-");
    assert_eq!(joined, "plot-meadow");
}

pub fn multiple_from_choices() {
    // `From` has multiple impls; target annotation selects one.
    let as_string: String = String::from("harvest");
    assert_eq!(as_string, "harvest");

    let as_vec: Vec<u8> = Vec::from("field".to_string());
    // Vec<u8> from String consumes bytes.
    assert_eq!(as_vec.len(), 5);

    // `Into` with target-directed selection.
    let value = 42_u32;
    let into_u64: u64 = value.into();
    assert_eq!(into_u64, 42);
}

pub fn numeric_fallback() {
    // Unsuffixed literals fallback to i32/f64 when unconstrained.
    let int_literal = 5;
    let _: i32 = int_literal;

    let float_literal = 3.0;
    let _: f64 = float_literal;

    // Suffix vs fallback distinguished.
    let explicit: u8 = 255_u8;
    assert_eq!(explicit, 255);

    // Affected by annotation.
    let with_annotation: u64 = 100;
    assert_eq!(with_annotation, 100_u64);
}

pub fn target_directed_selection() {
    // Target-directed associated projection.
    let source = "123";
    let number: i32 = source.parse().unwrap();
    assert_eq!(number, 123);

    // `collect` target changes output.
    let data = [1, 2, 3, 2, 1];
    let as_map: HashMap<i32, usize> = data.into_iter().fold(HashMap::new(), |mut acc, v| {
        *acc.entry(v).or_insert(0) += 1;
        acc
    });
    assert_eq!(as_map[&1], 2);

    // Annotation changes impl selection.
    let via_from_str = i32::from_str("9").unwrap();
    assert_eq!(via_from_str, 9);
}

pub fn ambiguous_and_no_implicit_conversion() {
    // No general implicit user conversion: explicit `From` is required.
    let n: i32 = 5;
    // let label: String = n; // would fail: no implicit conversion
    let label = n.to_string();
    assert_eq!(label, "5");

    // Constraining a generic associated projection.
    let values: Vec<u32> = vec![1, 2];
    let projected: Vec<String> = values.into_iter().map(|v| v.to_string()).collect();
    assert_eq!(projected.len(), 2);
}
