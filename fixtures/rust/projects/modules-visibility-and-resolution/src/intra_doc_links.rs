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

/// Hidden item link: [`HiddenDemo`] carries `#[doc(hidden)]`, yet an intra-doc
/// link to it resolves in the standard documentation build — a hidden item is
/// still a nameable path target, only omitted from the rendered index.
pub fn hidden_item_link() -> u32 {
    let _ = HiddenDemo { value: 2 };
    42
}

/// Restricted-visibility intra-doc links that resolve in the crate's
/// `--document-private-items` documentation build (see `Taskfile.yml`):
///
/// - [`crate::visibility_restricted::CrateVisible`] — a `pub(crate)` item.
/// - [`crate::visibility_restricted::sibling_a::SiblingCrateVisible`] — a
///   `pub(crate)` item in a sibling module.
/// - [`crate::visibility_restricted::ReachableCapped`] — the public re-export
///   through which the effectively-private `CappedPublic` (nested in the private
///   `private_container` module, so unnameable by its own path) is reached.
///
/// This function is itself private, so these links are checked only in the
/// private-items documentation build and never trigger `private_intra_doc_links`.
/// No broken-link lint is suppressed; the private-items build denies both
/// `broken_intra_doc_links` and `private_intra_doc_links`.
fn restricted_visibility_links() -> u32 {
    0
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
