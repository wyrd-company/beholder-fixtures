//! RS-CAN-PROJ-003: two aliased versions of `hyphen-crate` consumed together.
//! `hyphen_v2` (v0.2.0, `crates/hyphen-crate-v02`) and `hyphen_v3` (v0.3.0,
//! `crates/hyphen-crate-v03`) are both imported here via their dependency-key
//! aliases, never via either crate's own `[lib] name` — a renamed dependency's
//! extern name always follows the consumer's manifest key.

/// Holds both aliased versions' `HyphenType` side by side. Despite sharing the
/// source-level name `HyphenType`, `hyphen_v2::HyphenType` and
/// `hyphen_v3::HyphenType` are distinct nominal types (different crate
/// instances), so this struct needs two separate fields rather than one.
pub struct HyphenPair {
    pub v2: hyphen_v2::HyphenType,
    pub v3: hyphen_v3::HyphenType,
}

pub fn hyphen_pair() -> HyphenPair {
    HyphenPair {
        v2: hyphen_v2::library_fn(),
        v3: hyphen_v3::library_fn(),
    }
}

pub fn hyphen_versions() -> (&'static str, &'static str) {
    (hyphen_v2::VERSION, hyphen_v3::VERSION)
}

// Nominal mismatch counterexample (documented, not compiled): the two
// `HyphenType`s do not unify despite the identical source-level name.
// `let _: hyphen_v2::HyphenType = hyphen_v3::library_fn();`
// -> error[E0308]: mismatched types
//    expected struct `hyphen_v2::HyphenType`, found struct `hyphen_v3::HyphenType`
