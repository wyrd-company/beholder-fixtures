//! RS-CAN-TRAIT-006 — method lookup through deref chain, autoref, and unsizing.

use std::ops::Deref;

/// Leaf type in the deref chain.
pub struct Leaf {
    pub value: i32,
}

impl Leaf {
    pub fn leaf_method(&self) -> i32 {
        self.value
    }
    pub fn shared_name(&self) -> &'static str {
        "leaf"
    }
    pub fn shared_ref(&self) -> i32 {
        10
    }
    pub fn shared_mut_ref(&mut self) -> i32 {
        11
    }
}

/// Middle layer dereferences to Leaf.
pub struct Mid(pub Leaf);

impl Deref for Mid {
    type Target = Leaf;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl Mid {
    pub fn mid_method(&self) -> i32 {
        self.0.value + 1
    }
    pub fn shared_name(&self) -> &'static str {
        "mid"
    }
}

/// Outer layer dereferences to Mid, forming a chain Outer -> Mid -> Leaf.
/// `shared_name` on Outer shadows `Mid::shared_name` and `Leaf::shared_name`.
pub struct Outer(pub Mid);

impl Deref for Outer {
    type Target = Mid;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl Outer {
    pub fn outer_method(&self) -> i32 {
        self.0.0.value + 2
    }

    /// Wrapper shadowing: this inherent `shared_name` shadows the
    /// dereferenced `Mid::shared_name` and `Leaf::shared_name`.
    pub fn shared_name(&self) -> &'static str {
        "outer"
    }
}

/// Trait implemented for Leaf and for references to show T vs &T impls.
pub trait Greet {
    fn greet(&self) -> String;
}

impl Greet for Leaf {
    fn greet(&self) -> String {
        format!("Leaf {}", self.value)
    }
}

impl Greet for &Leaf {
    fn greet(&self) -> String {
        format!("&Leaf {}", self.value)
    }
}

/// Same-name `pick` with shared vs mutable receivers to demonstrate
/// candidate ordering: `&self` is tried before `&mut self`.
pub trait SharedPick {
    fn pick(&self) -> &'static str;
}

pub trait MutPick {
    fn pick(&mut self) -> &'static str;
}

impl SharedPick for Leaf {
    fn pick(&self) -> &'static str {
        "shared"
    }
}

impl MutPick for Leaf {
    fn pick(&mut self) -> &'static str {
        "mut"
    }
}

/// Unsizing demonstration: array coerced to slice, slice method dispatched.
pub fn lookup_summary() -> (
    i32,
    i32,
    i32,
    &'static str,
    String,
    String,
    &'static str,
    usize,
) {
    let outer = Outer(Mid(Leaf { value: 5 }));
    let via_deref_leaf = outer.leaf_method();
    let via_deref_mid = outer.mid_method();
    let via_deref_outer = outer.outer_method();
    // Wrapper shadowing: Outer's `shared_name` shadows Mid and Leaf.
    let shadowed = outer.shared_name();

    // T vs &T: distinct impls for `Leaf` and `&Leaf`.
    let leaf_val = Leaf { value: 1 };
    let greet_leaf = <Leaf as Greet>::greet(&leaf_val);
    let leaf_ref: &Leaf = &Leaf { value: 2 };
    let greet_ref = <&Leaf as Greet>::greet(&leaf_ref);

    // Shared vs mutable candidate ordering: both `SharedPick::pick(&self)`
    // and `MutPick::pick(&mut self)` are in scope, same name `pick`.
    // With a mutable leaf, `&self` candidate is considered before `&mut self`,
    // so the shared version wins.
    let mut leaf_mut = Leaf { value: 2 };
    let shared_pick = {
        use crate::lookup::{MutPick, SharedPick};
        // `MutPick` is in scope to make the `&mut self` candidate available,
        // but `SharedPick` wins due to autoref ordering.
        let _mut_candidate = MutPick::pick(&mut leaf_mut);
        let picked = SharedPick::pick(&leaf_mut);
        // The bare `pick` call demonstrates the ordering: it selects `SharedPick`.
        let bare = leaf_mut.pick();
        assert_eq!(bare, "shared");
        let _ = _mut_candidate;
        picked
    };

    // Unsizing: [i32; 3] dereferences/unsize to &[i32] for slice method `len`.
    let arr = [1, 2, 3];
    let arr_len = arr.len();
    // Also slice trait method via deref coercion: demonstrate slice handling
    let _slice: &[i32] = &arr;
    let _empty = _slice.is_empty();

    (
        via_deref_leaf,
        via_deref_mid,
        via_deref_outer,
        shadowed,
        greet_leaf,
        greet_ref,
        shared_pick,
        arr_len,
    )
}
