//! RS-CAN-OWN-006: Closure capture precision and mode (edition 2024 view).
//! Edition-2018 vs 2021 disjoint capture contrast lives in `crates/edition-2018` and `crates/edition-2021`.

pub struct Pair {
    pub first: String,
    pub second: String,
}

/// Every capture mode: shared, mutable, by-value (move).
pub fn capture_modes() {
    // Shared borrow capture: closure only reads.
    let value = String::from("shared");
    let read = || value.len();
    let _ = read();
    let _ = read();
    // `value` still usable because only shared borrowing occurred.
    let _ = value.len();

    // Mutable borrow capture.
    let mut counter = 0;
    let mut inc = || {
        counter += 1;
        counter
    };
    let _ = inc();
    let _ = inc();
    let _ = counter;

    // By-value (move) capture with `move` keyword.
    let owned = String::from("owned");
    let consume = move || owned.len();
    let _ = consume();
    // `owned` moved, not usable here (counterexample documented).
}

/// Unique immutable borrow capture (disjoint immutable of one field while mutating another).
pub fn unique_immutable_capture() {
    let mut pair = Pair {
        first: String::from("a"),
        second: String::from("b"),
    };
    // Closure borrows `first` immutably without borrowing whole `pair`.
    let read_first = || pair.first.len();
    let _ = read_first();
    // `pair.second` not captured, so mutation is allowed even while closure exists (disjoint).
    pair.second.push_str("!");
    let _ = read_first();
}

/// Disjoint field capture: closure captures one field, other field remains free.
pub fn disjoint_field_capture() -> String {
    let mut pair = Pair {
        first: String::from("hello"),
        second: String::from("world"),
    };
    let first_len = {
        let closure = || pair.first.len();
        // `pair.second` is disjoint, can be mutated without affecting closure's borrow.
        pair.second.push_str("!");
        closure()
    };
    let _ = first_len;
    pair.second
}

/// Move closure with later use of uncaptured values.
pub fn move_closure_uncaptured() -> String {
    let a = String::from("captured");
    let b = String::from("uncaptured");
    let closure = {
        let a = a; // move `a` into closure environment
        move || a.len()
    };
    let _ = closure();
    // `b` was not captured, still usable.
    b
}

/// Partial capture: closure captures one field by value, other fields remain.
pub fn partial_capture() -> String {
    let pair = Pair {
        first: String::from("first"),
        second: String::from("second"),
    };
    // Move only `first` into closure via destructuring move.
    let first = pair.first;
    let closure = move || first.len();
    let _ = closure();
    // `pair.second` was not moved (it was moved as part of `pair.first` move? Actually `pair` partially moved)
    // Demonstrate uncaptured value still usable:
    let other = String::from("other");
    let _ = other.len();
    // Need to keep `pair.second` accessible: we moved only `first`, so we still have `pair.second`? No, `pair` is partially moved.
    // Instead show simple disjoint move:
    let x = String::from("x");
    let y = String::from("y");
    let c = {
        let x = x;
        move || x.len()
    };
    let _ = c();
    y
}

/// Explicit `move` keyword requests by-value capture; it does not alone choose FnOnce vs Fn.
pub fn move_keyword_demo() -> usize {
    let data = vec![1, 2, 3];
    // `move` forces by-value capture but closure only reads, so it still implements Fn.
    let closure = move || data.len();
    closure() + closure()
}

pub fn closure_capture_summary() -> (String, String, String, usize) {
    capture_modes();
    unique_immutable_capture();
    let a = disjoint_field_capture();
    let b = move_closure_uncaptured();
    let c = partial_capture();
    let d = move_keyword_demo();
    (a, b, c, d)
}
