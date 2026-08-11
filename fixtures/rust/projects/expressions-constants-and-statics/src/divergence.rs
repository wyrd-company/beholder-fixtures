//! RS-CAN-EXPR-005 — Return, divergence, panic, and unreachable code.

/// Early return with value.
pub fn early_return(flag: bool) -> i32 {
    if flag {
        return 1;
    }
    if !flag {
        return 2;
    }
    0
}

/// Nonreturning function with `-> !`.
pub fn never_returns() -> ! {
    panic!("intentional divergent function");
}

/// Calls a `-> !` function in a coercion context (diverging branch coerces).
pub fn call_never_coercion(flag: bool) -> i32 {
    if flag { never_returns() } else { 10 }
}

/// Infinite loop that diverges until break, demonstrating `loop` as diverging before break.
///
/// The loop below never terminates except via `return` or `break`; valid diverging control.
pub fn infinite_loop_with_break(mut limit: i32) -> i32 {
    let result = loop {
        limit -= 1;
        if limit <= 0 {
            break 77;
        }
        if limit == 999 {
            // This branch would be infinite if taken; here it's just a guard.
            continue;
        }
    };
    result
}

/// Panic macro usage: `panic!`, `unreachable!`, `todo!` as divergent expressions.
pub fn panic_usages(flag: bool) -> i32 {
    if flag {
        panic!("explicit panic")
    }
    let val = if flag {
        unreachable!("should not reach with flag true")
    } else {
        5
    };
    val
}

/// Unreachable code after diverging expression: compiler sees dead code but type-checks it.
/// Note: unreachable-code lint is distinct from type validity.
#[allow(unreachable_code)]
pub fn unreachable_code_demo() -> i32 {
    let _pre = 1;
    // The branch below diverges; following code is unreachable but valid.
    if true {
        return 8;
    }
    // This is unreachable but still checked for type validity.
    let _unreachable: i32 = {
        // Even unreachable values must type-check.
        42
    };
    _unreachable
}

/// Closure with early return targeting the closure body (not outer function).
pub fn closure_return_target() -> i32 {
    let mut values = vec![1, 2, 3, 4];
    let mut closure = |x: i32| -> i32 {
        if x == 2 {
            return 99;
        }
        x * 2
    };
    let mapped: Vec<i32> = values.drain(..).map(|v| closure(v)).collect();
    mapped.iter().sum()
}

/// Never fallback: divergent expression can select type for inferred variable.
pub fn never_fallback_demo() -> i32 {
    // `!` coerces to `i32` here via branch.
    let val: i32 = if false { never_returns() } else { 7 };
    val
}

/// Infinite diverging loop helper used for lint illustration (never returns unless broken).
#[allow(dead_code)]
pub fn diverging_loop_only() -> ! {
    loop {
        std::hint::spin_loop();
    }
}

pub fn demonstrate() -> i32 {
    let _ = early_return(true);
    let _ = call_never_coercion(false);
    let _ = infinite_loop_with_break(3);
    let _ = panic_usages(false);
    let _ = unreachable_code_demo();
    let _ = closure_return_target();
    let _ = never_fallback_demo();
    1
}
