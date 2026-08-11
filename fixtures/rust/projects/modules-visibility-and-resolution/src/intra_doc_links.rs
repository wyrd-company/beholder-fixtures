// RS-CAN-MOD-014: intra-doc links to item, method, Self item, re-export, namespace-disambiguated entities.

/// Demonstrates linking to an item [`crate::reexports::InternalType`].
pub struct LinkDemo {
    pub value: u32,
}

impl LinkDemo {
    /// Links to method [`Self::linked_method`].
    pub fn linked_method(&self) -> u32 {
        self.value
    }

    /// Links to Self item [`Self::linked_method`] via Self.
    pub fn via_self_link(&self) -> u32 {
        self.linked_method()
    }
}

/// Links to re-export [`crate::reexports::RenamedType`] and original [`crate::reexports::implementation::InternalType`].
pub fn link_to_reexport() -> crate::reexports::RenamedType {
    crate::reexports::RenamedType::new(1)
}

/// Namespace-disambiguated links: type [`LinkDemo`] vs value [`crate::namespaces::alpha`] vs macro [`crate::alpha!`].
///
/// - Type namespace: [`LinkDemo`]
/// - Value namespace: [`crate::namespaces::alpha`]
/// - Macro namespace: [`crate::alpha!`]
pub fn namespace_links() -> u32 {
    0
}

/// Link to associated item via Self: [`LinkDemo::linked_method`] (same as `Self::linked_method` when in impl).
pub fn self_item_link_demo() -> u32 {
    let d = LinkDemo { value: 5 };
    d.linked_method()
}

/// Private item link (rustdoc can link but lint warns): private type not linked here to avoid warning.
/// Cross-module link: [`crate::glob_ambiguity::source_a::CollidingType`].
pub fn cross_module_link() -> u32 {
    42
}

/// Link to re-exported dependency type [`crate::reexports::ReexportedDirectType`].
pub fn dependency_reexport_link() -> crate::reexports::ReexportedDirectType {
    crate::reexports::ReexportedDirectType::new(10)
}

// Broken link counterexample is documented in `docs/counterexamples.md` and not present as a real link here,
// because a broken `/// [`nonexistent::Item`]` would cause `cargo doc` warning/deny failure.
// Valid contrast: this file's links all resolve.
