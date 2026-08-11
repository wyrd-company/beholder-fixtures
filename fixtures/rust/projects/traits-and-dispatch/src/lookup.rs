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

/// Demonstrates &self vs &mut self candidate ordering: &self candidate
/// is considered earlier than &mut self, so immutable borrow wins when both viable.
pub trait MutChoice {
    fn choose(&self) -> &'static str;
    fn choose_mut(&mut self) -> &'static str;
}

impl MutChoice for Leaf {
    fn choose(&self) -> &'static str {
        "shared"
    }
    fn choose_mut(&mut self) -> &'static str {
        "mut"
    }
}

/// Unsizing demonstration: array coerced to slice, slice method dispatched.
pub fn lookup_summary() -> (i32, i32, i32, String, String, &'static str, usize) {
    let outer = Outer(Mid(Leaf { value: 5 }));
    let via_deref_leaf = outer.leaf_method();
    let via_deref_mid = outer.mid_method();
    let via_deref_outer = outer.outer_method();
    // Autoderef + autoref: methods taking &self can be called on owned Outer via autoref.
    // The chain Outer -> Mid -> Leaf allows leaf_method through deref.
    // Shadowing: Outer's inherent shadowing if same name existed is not used here; we demonstrate via explicit chain.
    let greet_leaf = Leaf { value: 1 }.greet();
    let leaf_val = Leaf { value: 1 };
    let leaf_ref: &Leaf = &leaf_val;
    let greet_ref = leaf_ref.greet();

    // &self vs &mut self: calling on mutable leaf with immutable context selects shared.
    let leaf_mut = Leaf { value: 2 };
    let choice = leaf_mut.choose();

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
        greet_leaf,
        greet_ref,
        choice,
        arr_len,
    )
}
