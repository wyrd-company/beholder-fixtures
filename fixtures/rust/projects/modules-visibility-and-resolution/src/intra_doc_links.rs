// RS-CAN-MOD-014: intra-doc links to item, method, Self item, re-export, namespace-disambiguated entities.

/// Link to item [`crate::reexports::InternalType`].
pub struct LinkDemo {
    pub value: u32,
}

impl LinkDemo {
    /// Link to method [`Self::linked_method`] via Self.
    pub fn linked_method(&self) -> u32 {
        self.value
    }

    /// Link to Self item [`Self::linked_method`] explicitly via Self.
    pub fn via_self_link(&self) -> u32 {
        self.linked_method()
    }
}

/// Link to re-export [`crate::reexports::RenamedType`] and original via public re-export [`crate::reexports::InternalType`] (original `implementation` is private, bypassed via `ReachableCapped` style re-export).
/// Demonstrates `#[doc(inline)]` vs `#[doc(no_inline)]` presentation variants are in `src/reexports.rs`.
pub fn link_to_reexport() -> crate::reexports::RenamedType {
    crate::reexports::RenamedType::new(1)
}

/// Namespace-disambiguated links for same spelling `demo` across type, value, and macro namespaces.
///
/// - Type: [`struct@crate::namespaces::demo`] (struct `demo`)
/// - Value: [`crate::namespaces::demo()`] (function `demo()`)
/// - Macro: [`crate::demo!`] (bang macro `demo!` via `#[macro_export]`)
///
/// Each uses explicit disambiguator `struct@`, `()` or `!` for same identifier `demo`.
pub fn namespace_disambiguated_links() -> u32 {
    let t = crate::namespaces::demo { v: 1 };
    let v = crate::namespaces::demo();
    let m = crate::demo!();
    t.v + v + m
}

/// Link to Self associated item from outside impl: [`LinkDemo::linked_method`].
pub fn self_item_link_demo() -> u32 {
    let d = LinkDemo { value: 5 };
    d.linked_method()
}

/// Private item link: [`crate::visibility_restricted::private_container::CappedPublic`] is `pub` but effective visibility is private via `mod private_container`; [`crate::visibility_restricted::CrateVisible`] (`pub(crate)`) is crate-restricted.
/// Hidden item link: [`crate::intra_doc_links::HiddenDemo`] is `#[doc(hidden)]` but still linkable.
/// Cross-module link: [`crate::glob_ambiguity::source_a::CollidingType`].
#[allow(rustdoc::private_intra_doc_links, rustdoc::broken_intra_doc_links)]
pub fn private_and_hidden_links() -> u32 {
    let _ = HiddenDemo { value: 2 };
    42
}

/// `#[doc(hidden)]` item – hidden from docs but linkable for RS-CAN-MOD-014.
#[doc(hidden)]
pub struct HiddenDemo {
    pub value: u32,
}

/// Link to re-exported dependency type [`crate::reexports::ReexportedDirectType`].
pub fn dependency_reexport_link() -> crate::reexports::ReexportedDirectType {
    crate::reexports::ReexportedDirectType::new(10)
}

/// Cross-module link via glob re-export: [`crate::glob_ambiguity::source_a::CollidingEnum::VariantA`].
pub fn cross_module_enum_link() -> crate::glob_ambiguity::source_a::CollidingEnum {
    crate::glob_ambiguity::source_a::CollidingEnum::VariantA
}

// Broken link counterexample documented in `docs/counterexamples.md`, not present as failing link here.
