//! RS-CAN-MOD-003: type, value, macro, lifetime, label namespaces resolved from shared spelling.

// Type namespace: struct named `alpha`.
pub struct Alpha {
    pub v: u32,
}

// Value namespace: function and const also named `alpha` (value namespace).
pub fn alpha() -> u32 {
    1
}

pub const alpha_const: u32 = 2;

// Unit struct with same spelling as function would collide in value namespace - demonstrate distinct forms:
// Tuple struct creates value constructor in value namespace.
pub struct Beta(pub u32);

// Named-field struct does NOT create callable value constructor; its path is type-only.
pub struct Gamma {
    pub x: u32,
}

// Macro namespace: macro_rules! also named `alpha` lives in macro namespace, separate from type/value.
#[macro_export]
macro_rules! alpha {
    () => {
        99
    };
}

// Derive/attribute/bang macro distinctions are macro-namespace variants (documented as distinct).
// Built-in derive macros live in same macro namespace but are resolved via attribute path.

// Lifetime namespace vs loop label namespace example:
pub fn lifetime_and_label_demo<'alpha>(input: &'alpha str) -> &'alpha str {
    // Lifetime `'alpha` is in lifetime namespace; loop label `'alpha` would be label namespace.
    // Same spelling can appear as both lifetime and label without conflict.
    let result = 'alpha: loop {
        break 'alpha input;
    };
    result
}

// Function demonstrating lifetime and label same spelling distinct namespaces:
pub fn label_namespace_demo() -> u32 {
    'alpha: for i in 0..3 {
        if i == 1 {
            break 'alpha;
        }
    }
    3
}

// Value namespace vs type namespace usage disambiguated by context:
pub fn namespace_resolution_demo() -> u32 {
    // `Alpha` as type
    let _typed: Alpha = Alpha { v: 5 };
    // `alpha` as value (function)
    let _valued = alpha();
    // `alpha!` as macro
    let _macroed = crate::alpha!();
    // Lifetime usage
    let s = "hello";
    let _lifetimed = lifetime_and_label_demo(s);
    let _labeled = label_namespace_demo();
    _typed.v + _valued + _macroed + _labeled
}

// Distinct type/value import interaction: importing can introduce bindings into multiple namespaces.
// Example: `use crate::namespaces::Alpha;` imports type, while `use crate::namespaces::alpha;` imports value.
