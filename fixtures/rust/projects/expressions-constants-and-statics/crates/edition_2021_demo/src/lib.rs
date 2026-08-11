//! Edition 2021 contrast: temporary scope and `if let` / let-chain availability.
//!
//! On edition 2021, let chains are not available (require edition 2024).
//! This crate documents the 2021 behavior and provides a valid analogue.

/// `if let` with temporary scope as handled in edition 2021.
///
/// The temporary `String` created for `as_ref` handling has the 2021 rescoping.
/// This function compiles in edition 2021 and mirrors the 2024 tail-scope contrast
/// documented in `blocks` and `conditionals`.
pub fn if_let_temporary_scope_2021() -> Option<usize> {
    let maybe = Some(String::from("field"));
    if let Some(s) = maybe.as_ref().map(|s| s.clone()) {
        Some(s.len())
    } else {
        None
    }
}

/// Traditional `if let` chain alternative without `&&` let chain syntax.
///
/// On edition 2021, the let-chain `if let Some(x) = a && let Some(y) = b` is not valid.
/// Equivalent nesting is used instead.
pub fn nested_if_let_alternative(a: Option<i32>, b: Option<i32>) -> Option<i32> {
    if let Some(x) = a {
        if let Some(y) = b {
            return Some(x + y);
        }
    }
    None
}

/// Tail temporary scope analogue in edition 2021.
///
/// Demonstrates that block tail temporaries had different lifetime handling pre-2024.
pub fn tail_temporary_2021() -> usize {
    let len = {
        let s: &str = &String::from("harvest");
        s.len()
    };
    len
}

pub fn demonstrate() -> i32 {
    let _ = if_let_temporary_scope_2021();
    let _ = nested_if_let_alternative(Some(1), Some(2));
    let _ = tail_temporary_2021();
    1
}
