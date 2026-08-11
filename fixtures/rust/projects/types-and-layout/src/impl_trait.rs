//! RS-CAN-TYPE-010 — argument- and return-position `impl Trait`.

use std::fmt::Display;

// Argument-position `impl Trait` as anonymous generic.
pub fn takes_impl(value: impl Display) -> String {
    format!("{value}")
}

// Named generic twin.
pub fn takes_generic<T: Display>(value: T) -> String {
    format!("{value}")
}

// Return-position `impl Trait` returning one concrete iterator.
#[allow(clippy::if_same_then_else)]
pub fn make_iter() -> impl Iterator<Item = i32> {
    // Both branches produce the same concrete type by selecting the range first.
    let use_even = true;
    let base = if use_even { 0..5 } else { 0..5 };
    base.map(|x| x * 2)
}

// Distinct hidden types from different definitions.
pub fn make_chars() -> impl Iterator<Item = char> {
    "meadow".chars()
}

pub fn distinct_hidden_types() {
    // Caller cannot turbofish an `impl Trait` return.
    let iter = make_iter();
    let sum: i32 = iter.sum();
    assert_eq!(sum, 20);

    // Each function has its own hidden type, so mixing iterators is explicit.
    let _first = make_iter();
    let _second = make_chars();
    // let _mix: Vec<i32> = first.chain(second).collect(); // would fail: different item types
}

// Nested opaque use: `impl Trait` capturing another `impl Trait`.
pub fn nested_opaque(values: Vec<i32>) -> impl Iterator<Item = String> {
    values.into_iter().map(|v| v.to_string())
}

// Auto-trait leakage example: returned opaque future/iter may capture Send etc.
pub fn opaque_send_preserved() -> impl Iterator<Item = i32> + Send {
    vec![1, 2, 3].into_iter()
}

pub fn auto_trait_leakage_demo() {
    let iter = opaque_send_preserved();
    // The returned opaque type is Send; transferring across threads conceptually
    // preserves that bound.
    let _send: Box<dyn Send> = Box::new(iter);
}

pub fn capture_examples() {
    let prefix = "plot-".to_string();
    // RPIT captures shared data by move.
    let labeled = make_labeled_iter(prefix, vec![1, 2, 3]);
    assert_eq!(labeled.count(), 3);
}

fn make_labeled_iter(prefix: String, values: Vec<i32>) -> impl Iterator<Item = String> {
    values.into_iter().map(move |v| format!("{prefix}{v}"))
}
