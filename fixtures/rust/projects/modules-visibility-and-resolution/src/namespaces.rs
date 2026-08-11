// RS-CAN-MOD-003: type, value, macro, lifetime, label namespaces resolved from shared spelling.

// Shared spelling `demo` across type, value, macro, lifetime, label namespaces.
// Type namespace: named-field struct `demo` (no value constructor, so value `demo` function can coexist).
#[allow(non_camel_case_types)]
pub struct demo {
    pub v: u32,
}

// Value namespace: function `demo` and const `demo` would share value namespace with struct constructor if tuple.
// But `demo` struct has named fields, so no constructor in value namespace; `demo()` is a distinct value binding.
pub fn demo() -> u32 {
    1
}

// Additional value namespace const with distinct name to avoid value collision with `demo()`.
// The shared spelling demonstration uses `demo` type vs `demo` function; const uses `DEMO_CONST`.
pub const DEMO_VALUE: u32 = 2;

// Value namespace collision illustration: tuple struct introduces constructor.
// Tuple struct `Beta` creates type `Beta` and value constructor `Beta` (value namespace).
pub struct Beta(pub u32);

// Named-field struct `Gamma` has type `Gamma` but no value constructor.
pub struct Gamma {
    pub x: u32,
}

// Derive macro namespace variant: `Debug` is a derive macro (proc-macro derive).
#[derive(Debug, Clone)]
pub struct DemoDerive {
    pub x: u32,
}

// Attribute macro variant: `inline` is an attribute (built-in attribute macro).
#[inline]
pub fn demo_inline_attr() -> u32 {
    3
}

// Attribute with derive helper style: `allow` is a tool/attribute namespace variant.
#[allow(dead_code)]
pub fn demo_allow_attr() -> u32 {
    4
}

// Bang macro namespace: same spelling `demo` as type/value, but in macro namespace.
#[macro_export]
macro_rules! demo {
    () => {
        99
    };
}

// Lifetime and label namespaces sharing same spelling `'demo`.

pub fn lifetime_and_label_demo<'demo>(input: &'demo str) -> &'demo str {
    // Lifetime `'demo` in lifetime namespace; loop label `'demo` in label namespace – same spelling, distinct namespaces.
    let result = 'demo: loop {
        break 'demo input;
    };
    result
}

pub fn label_namespace_demo() -> u32 {
    'demo: for i in 0..3 {
        if i == 1 {
            break 'demo;
        }
    }
    3
}

// Combined resolution of shared spelling `demo` across all five namespaces.
pub fn namespace_resolution_demo() -> u32 {
    // `demo` as type (struct)
    let typed: demo = demo { v: 5 };
    // `demo` as value (function)
    let valued = demo();
    // `demo!` as macro (bang)
    let macroed = crate::demo!();
    // Lifetime `'demo`
    let s = "hello";
    let lifetimed = lifetime_and_label_demo(s);
    let _ = lifetimed;
    let labeled = label_namespace_demo();
    // `#[derive(Debug)]` type `DemoDerive` and attribute `demo_inline_attr` demonstrate derive/attribute macro namespaces.
    let _derived = DemoDerive { x: 1 };
    let _attr = demo_inline_attr();
    typed.v + valued + macroed + labeled + _derived.x + _attr
}

// Import of same spelling into multiple namespaces: `use crate::namespaces::demo` brings type,
// `use crate::namespaces::demo as _` would be trait/macro? But type vs value demonstration:
// `Beta` imported brings both type and constructor value when globbed? The following shows multi-namespace import:
pub mod import_demo {
    use crate::namespaces::Beta;
    use crate::namespaces::Gamma;

    pub fn uses_multi_namespace() -> (Beta, Gamma) {
        // `Beta` as type and as constructor value (tuple struct)
        let b: Beta = Beta(10);
        let g: Gamma = Gamma { x: 11 };
        (b, g)
    }
}
