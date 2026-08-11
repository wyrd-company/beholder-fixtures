//! RS-CAN-EXPR-003 — Conditional expressions, `if let`, and let chains (edition 2024).

/// Value-producing `if` expression where both arms coerce to one type.
pub fn value_producing_if(flag: bool) -> i32 {
    let value = if flag { 10 } else { 20 };
    value
}

/// `if` with coercion to a common type (integer coercion and branch compatibility).
pub fn if_coercion(flag: bool) -> i64 {
    if flag { 1_i32 as i64 } else { 2_i64 }
}

/// Scoped `if let` where pattern bindings are only available in the successful region and
/// temporaries are scoped accordingly (2024 temporary rescoping).
pub fn scoped_if_let(input: Option<String>) -> usize {
    if let Some(text) = input {
        // `text` is bound only here.
        text.len()
    } else {
        0
    }
}

/// Demonstrates `if let` temporary scope contrast: in edition 2024, temporaries in `if let` condition
/// are handled with the new scope. This valid code compiles in both editions but illustrates the
/// intended edition-sensitive behavior documented in the 2021 companion crate.
pub fn if_let_temporary_scope() -> Option<usize> {
    let maybe = Some(String::from("field"));
    if let Some(s) = maybe.as_ref().map(|s| s.clone()) {
        Some(s.len())
    } else {
        None
    }
}

/// Let chain with short-circuit and binding behavior on edition 2024.
///
/// Valid only on edition 2024 (Rust 1.88+). Short-circuit: later segments are not evaluated if an
/// earlier let pattern fails or boolean is false. Bindings are introduced sequentially and only if prior
/// segments succeed.
pub fn let_chain_demo(a: Option<i32>, b: Option<i32>, flag: bool) -> Option<i32> {
    if let Some(x) = a
        && let Some(y) = b
        && flag
        && x < y
    {
        Some(x + y)
    } else {
        None
    }
}

/// Let chain showing binding unavailable after a failed segment.
pub fn let_chain_binding_unavailable(a: Option<i32>, b: Option<i32>) -> i32 {
    if let Some(x) = a
        && let Some(y) = b
    {
        x + y
    } else {
        // `x` and `y` are not available here (demonstrates scope).
        0
    }
}

/// While-like let chain contrast (valid in edition 2024 context as a loop condition alternative).
pub fn while_let_chain_like(inputs: Vec<Option<i32>>) -> i32 {
    let mut sum: i32 = 0;
    for item in inputs {
        if let Some(v) = item
            && v > 0
        {
            sum += v;
        }
    }
    sum
}

/// Short-circuit demonstration with side effects to show later chain segments not evaluated.
pub fn let_chain_short_circuit(side_effect: &mut bool) -> bool {
    let opt: Option<i32> = None;
    // Second segment should not run if first let fails; we track via `flag_fn`.
    if let Some(_x) = opt
        && flag_fn(side_effect)
    {
        true
    } else {
        false
    }
}

fn flag_fn(flag: &mut bool) -> bool {
    *flag = true;
    true
}

pub fn demonstrate() -> i32 {
    let _ = value_producing_if(true);
    let _ = value_producing_if(false);
    let _ = if_coercion(true);
    let _ = scoped_if_let(Some(String::from("harvest")));
    let _ = if_let_temporary_scope();
    let _ = let_chain_demo(Some(2), Some(5), true);
    let _ = let_chain_binding_unavailable(Some(1), Some(2));
    let _ = while_let_chain_like(vec![Some(3), None, Some(4)]);
    let mut flag = false;
    let _ = let_chain_short_circuit(&mut flag);
    assert!(!flag, "short-circuit should prevent second segment");
    1
}
