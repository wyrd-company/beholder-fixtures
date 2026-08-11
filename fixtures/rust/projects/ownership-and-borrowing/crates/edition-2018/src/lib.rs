//! Edition 2018 member: closure capture precision (whole capture) contrast.
//! RS-CAN-OWN-006 requires editions 2018 and 2021 for capture precision.

#![allow(dead_code)]

pub struct Pair {
    pub first: String,
    pub second: String,
}

/// In edition 2018 closures capture whole places, not disjoint fields.
/// Borrowing one field may borrow the entire struct for the closure's lifetime.
/// This function is valid in 2018 by avoiding disjoint mutation while closure is live.
pub fn capture_2018_whole() -> usize {
    let mut pair = Pair {
        first: String::from("hello"),
        second: String::from("world"),
    };
    // Closure captures `pair.first` but in 2018 this captures the whole `pair`.
    let len = {
        let closure = || pair.first.len();
        // In 2018, `pair.second` is considered borrowed through whole-capture,
        // so we do not mutate `pair.second` while closure is live.
        // Mutation after closure's last use is valid (NLL still applies).
        let l = closure();
        // Closure's borrow ends after last call; now mutation allowed.
        pair.second.push_str("!");
        l
    };
    len + pair.second.len()
}

/// Move closure in 2018: `move` requests by-value capture.
pub fn move_closure_2018() -> usize {
    let data = String::from("edition-2018");
    let closure = move || data.len();
    closure()
}

/// Disjoint field theory counterexample is documented: in 2018 disjoint mutation
/// like `let c = || pair.first.len(); pair.second = ...; c()` would be considered
/// overlapping and rejected on this edition, while it is accepted in 2021+.
/// See `docs/counterexamples.md` in the root crate.

pub fn edition_id() -> &'static str {
    "2018"
}
