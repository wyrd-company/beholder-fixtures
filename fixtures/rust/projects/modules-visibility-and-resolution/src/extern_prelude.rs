// RS-CAN-MOD-010: extern prelude, direct nameability, unnameable transitive, extern crate variants.

// Direct dependency is nameable via extern prelude without `extern crate`.
use fixture_direct::TransitiveType as DirectReexported;
use fixture_direct::{DirectType, ReexportedTransitive};

// Alias crate already declared in lib.rs: `renamed_dep` and `mvr_self`.
// Use them here without redeclaring.

// Direct nameability: using extern-prelude name `fixture_direct` and remapped `renamed_dep`.
pub fn uses_direct_via_prelude() -> DirectType {
    DirectType::new(10)
}

pub fn uses_direct_via_renamed() -> renamed_dep::DirectType {
    renamed_dep::DirectType::new(11)
}

pub fn uses_alloc_crate() -> alloc::vec::Vec<u32> {
    let mut v = alloc::vec::Vec::new();
    v.push(42);
    v
}

pub fn uses_self_alias() -> u32 {
    // `mvr_self::reexports::InternalType` via self alias reaches same crate.
    mvr_self::reexports::InternalType::new(12).value
}

// Transitive crate `fixture_transitive` is NOT directly nameable here without re-export.
// `TransitiveType` via `fixture_direct::TransitiveType` is nameable because direct_dep re-exports it.
// Direct path `fixture_transitive::TransitiveType` would fail (unnameable) - documented in counterexamples.
pub fn uses_transitive_via_reexport() -> DirectReexported {
    DirectReexported::new(13)
}

pub fn uses_reexported_transitive() -> fixture_direct::TransitiveType {
    fixture_direct::TransitiveType::new(14)
}

// Version skew: two versions of same logical crate via alias keys `skew_v1` / `skew_v2`.
pub fn skew_versions() -> (u32, u32) {
    (skew_v1::SKEW_CONST, skew_v2::SKEW_CONST)
}

pub fn skew_types_hold_both() -> (skew_v1::SkewType, skew_v2::SkewType) {
    (skew_v1::SkewType::new(), skew_v2::SkewType::new())
}

// Macro_use legacy case is in `crates/edition2015`; here we use modern `use` import for direct's macro.
use fixture_direct::direct_macro;

pub fn modern_macro_use() -> u32 {
    direct_macro!()
}

// Also demonstrate `extern crate alloc` type usage with allocation.
pub fn alloc_boxed() -> alloc::boxed::Box<u32> {
    alloc::boxed::Box::new(99)
}

// Unnameable transitive type: direct use without re-export would be `fixture_transitive::TransitiveType`.
// The following would fail: `let x = fixture_transitive::TransitiveType::new(1);` (unnameable).
// Valid access must go through `fixture_direct::TransitiveType`.
pub fn transitive_only_via_reexport() -> ReexportedTransitive {
    ReexportedTransitive::new(5)
}
