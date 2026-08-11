//! RS-CAN-TRAIT-012 — drop glue, Copy versus Clone.

use std::mem::{ManuallyDrop, forget};

/// Inner type with Drop for observing drop order.
pub struct Inner(pub &'static str);

impl Drop for Inner {
    fn drop(&mut self) {}
}

/// Outer contains multiple fields to demonstrate field drop order.
pub struct Outer {
    pub first: Inner,
    pub second: Inner,
    pub value: i32,
}

impl Drop for Outer {
    fn drop(&mut self) {}
}

/// Nested structure for nested drop order.
pub struct Nested {
    pub outer: Outer,
    pub extra: Inner,
}

impl Drop for Nested {
    fn drop(&mut self) {}
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Copyable(pub i32);

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NonCopy(pub String);

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DerivedCloneDemo(pub String);

/// Manual `Clone` implementation on a contrasting type.
pub struct ManualCloneDemo(pub String);

impl Clone for ManualCloneDemo {
    fn clone(&self) -> Self {
        Self(self.0.clone())
    }
}

impl std::fmt::Debug for ManualCloneDemo {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_tuple("ManualCloneDemo").field(&self.0).finish()
    }
}

impl PartialEq for ManualCloneDemo {
    fn eq(&self, other: &Self) -> bool {
        self.0 == other.0
    }
}

impl Eq for ManualCloneDemo {}

/// Helper without Drop to demonstrate partial moves.
pub struct MoveDemo {
    pub a: String,
    pub b: String,
    pub c: i32,
}

pub fn drop_summary() -> String {
    // Nested and field drop order exercised.
    let _nested = Nested {
        outer: Outer {
            first: Inner("first"),
            second: Inner("second"),
            value: 1,
        },
        extra: Inner("extra"),
    };

    // Explicit drop.
    let to_drop = Inner("explicit");
    drop(to_drop);

    // Partial moves on a non-Drop type succeed.
    let outer_move = MoveDemo {
        a: "a".to_owned(),
        b: "b".to_owned(),
        c: 2,
    };
    let moved_a = outer_move.a;
    let _ = moved_a;
    let _remaining_b = outer_move.b;
    let _remaining_c = outer_move.c;
    // Counterexample (invalid, documented in docs/counterexamples.md):
    // Moving a field out of a Drop type is rejected:
    // `let outer = Outer { first: Inner("a"), second: Inner("b"), value: 2 };`
    // `let _ = outer.first; // error[E0509]: cannot move out of type Outer which implements Drop`

    // ManuallyDrop suppresses automatic drop.
    let manual = ManuallyDrop::new(Inner("manual"));
    let _inner_ref: &Inner = &manual;
    // Need to avoid drop; ManuallyDrop will not run destructor automatically.
    // Explicit forget also suppresses drop.
    let forgotten = Inner("forget");
    forget(forgotten);

    // Copy versus Clone use-after-assignment.
    let copy_val = Copyable(10);
    let copy_two = copy_val;
    let _use_both = copy_val.0 + copy_two.0;

    let non_copy = NonCopy("hello".to_owned());
    let moved = non_copy;
    // let _ = non_copy; // would be rejected: use after move.
    let cloned = moved.clone();
    let _use_moved_and_clone = format!("{} {}", moved.0, cloned.0);

    // Manual versus derived Clone exercised beside each other.
    let derived = DerivedCloneDemo("world".to_owned());
    let derived_cloned = derived.clone();
    let manual = ManualCloneDemo("world".to_owned());
    let manual_cloned = manual.clone();
    format!(
        "{}|{}|{}|{}",
        derived.0, derived_cloned.0, manual.0, manual_cloned.0
    )
}
