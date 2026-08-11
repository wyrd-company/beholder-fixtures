//! RS-CAN-OWN-007: `Fn`, `FnMut`, and `FnOnce`.

fn call_fn<F: Fn() -> usize>(f: F) -> usize {
    f() + f()
}

fn call_fn_mut<F: FnMut() -> usize>(mut f: F) -> usize {
    f() + f()
}

fn call_fn_once<F: FnOnce() -> usize>(f: F) -> usize {
    f()
}

/// Reading closure satisfies `Fn`.
pub fn reading_closure_fn() -> usize {
    let value = String::from("read");
    let closure = || value.len();
    call_fn(closure)
}

/// Mutating closure satisfies `FnMut`.
pub fn mutating_closure_fnmut() -> usize {
    let mut counter = 0;
    let closure = || {
        counter += 1;
        counter
    };
    call_fn_mut(closure)
}

/// Consuming closure satisfies `FnOnce` only: the body moves `data` out
/// via `into_bytes`, so the closure cannot implement `Fn` or `FnMut`.
pub fn consuming_closure_fnonce() -> usize {
    let data = String::from("consume");
    let closure = move || data.into_bytes().len();
    call_fn_once(closure)
}

/// Move closure that still implements `Fn` (captured value is moved but only read).
pub fn move_still_fn() -> usize {
    let data = String::from("still-fn");
    let closure = move || data.len();
    // `data` moved, but closure body only reads it, so it is Fn.
    call_fn(closure)
}

/// Non-capturing closure coerces to function pointer.
pub fn noncapturing_fn_pointer() -> i32 {
    let closure = |x: i32| x + 1;
    let ptr: fn(i32) -> i32 = closure;
    ptr(41)
}

/// Copy/Clone closure traits: non-capturing and shared-capturing closures are Copy.
pub fn copy_clone_closure() -> usize {
    let value = 10;
    let closure = || value + 1; // captures `value` by shared ref, Copy
    let c2 = closure;
    let _ = c2();
    closure() + c2()
}

/// Consuming closure cannot satisfy `Fn` bound — documented as counterexample in `docs/counterexamples.md`.
/// Example invalid: `call_fn(move || { let s = String::new(); drop(s); 0 })` where closure moves non-Copy value out.

pub fn call_traits_summary() -> (usize, usize, usize, usize, i32, usize) {
    let a = reading_closure_fn();
    let b = mutating_closure_fnmut();
    let c = consuming_closure_fnonce();
    let d = move_still_fn();
    let e = noncapturing_fn_pointer();
    let f = copy_clone_closure();
    (a, b, c, d, e, f)
}
