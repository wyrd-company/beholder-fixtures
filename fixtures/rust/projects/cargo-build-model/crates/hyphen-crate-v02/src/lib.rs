#![allow(dead_code)]

//! RS-CAN-PROJ-003: distinct package, library, executable, and dependency-key names.
//! Package name is `hyphen-crate` (hyphen); this version's library takes Cargo's
//! default hyphen-to-underscore mapping (`hyphen_crate`, no `[lib] name` override);
//! executable is `hyphen-executable`; dependency key in consumers is `hyphen_v2`.

pub struct HyphenType(pub u32);

pub fn library_fn() -> HyphenType {
    HyphenType(200)
}

// Two versions under aliases: this is v0.2.0; v0.3.0 is in hyphen-crate-v03.
pub const VERSION: &str = "0.2.0";

/// Demonstrates `package =` vs local name: a consumer writes
/// `hyphen_v2 = { package = "hyphen-crate", path = "...v02" }` in its manifest,
/// then imports via the dependency key `use hyphen_v2::HyphenType` in source.
/// The extern name a consumer uses always follows its own manifest key (or
/// `package =` rename), never this crate's own `[lib] name` — see
/// `src/hyphen_identity.rs` for the real consuming code and `coverage.md` for
/// the registry-spelled-identifier counterexample.
pub fn via_package_name() -> HyphenType {
    HyphenType(202)
}
