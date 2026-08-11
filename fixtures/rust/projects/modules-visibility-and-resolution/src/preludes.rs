// RS-CAN-MOD-011: standard, core, extern, macro-use, language preludes.

// RS-CAN-MOD-011 fixture: unqualified prelude types/traits resolve without import.
pub struct PreludeDemo {
    // `Vec` from std prelude - unqualified.
    pub items: Vec<u32>,
    // `Option` from prelude.
    pub maybe: Option<u32>,
}

// Trait from prelude: `Copy` etc. but we demonstrate `Iterator` trait via prelude?
pub fn prelude_unqualified_types() -> (Vec<u32>, Option<u32>, String) {
    let v: Vec<u32> = Vec::new();
    let opt: Option<u32> = None;
    let s: String = String::from("hello");
    (v, opt, s)
}

// `core` vs `std` explicit paths still resolve to same entities when std is available.
pub fn core_vs_std_paths() -> (core::option::Option<u32>, std::option::Option<u32>) {
    (None, None)
}

pub fn prelude_trait_usage(v: Vec<u32>) -> usize {
    v.len()
}

// Local shadow of prelude item.
pub mod shadow_demo {
    // This local `Vec` shadows `std::vec::Vec` within this module.
    pub struct Vec {
        pub shadowed: u32,
    }

    pub fn uses_shadowed() -> Vec {
        Vec { shadowed: 1 }
    }

    pub fn accesses_true_vec_via_alloc() -> alloc::vec::Vec<u32> {
        alloc::vec::Vec::new()
    }

    pub fn accesses_true_vec_via_std() -> std::vec::Vec<u32> {
        std::vec::Vec::new()
    }
}

// Edition addition: example of an item added in a later edition/stdlib version.
pub fn edition_addition_demo(opt: Option<u32>) -> bool {
    opt.is_some_and(|x| x > 0)
}

// Language prelude: `Copy`, `Send`, `Sync`, `Sized`, `Unpin`, `Fn*`, drop, etc.
pub fn static_lifetime_demo(x: &'static str) -> &'static str {
    x
}

// Built-in/tool attributes as language prelude effects.
#[allow(dead_code)]
#[rustfmt::skip]
pub fn attribute_prelude_demo() -> u32 { 42 }

// `no_implicit_prelude` module - ordinary prelude imports removed.
#[no_implicit_prelude]
pub mod no_prelude_mod {
    // No implicit `std` prelude here; `Vec` would be unresolved without explicit path.

    extern crate std;

    pub fn without_prelude() -> std::vec::Vec<::core::primitive::u32> {
        std::vec::Vec::new()
    }

    // `core` prelude also missing: `Option` requires path.
    pub fn option_without_prelude() -> ::core::option::Option<::core::primitive::u32> {
        ::core::option::Option::None
    }
}

// Extern prelude vs std prelude distinction.
pub fn extern_vs_std_prelude() -> fixture_direct::DirectType {
    fixture_direct::DirectType::new(20)
}
