//! Cargo build model fixture root library.
//! Demonstrates RS-CAN-PROJ-001, 002, 019, 021, 022, 015 among others.

pub mod build_identity;
pub mod config_variant;
pub mod crate_type_demo;
#[path = "disabled/mod.rs"]
pub mod disabled;
pub mod dual_identity;
pub mod hyphen_identity;
pub mod profile_observables;
pub mod test_cfg;

// RS-CAN-PROJ-019: one source compiled under two invocation variants.
// `cargo_config_flag` is supplied via `.cargo/config.toml` build.rustflags,
// `target_config_flag` via target-specific rustflags, and RUSTFLAGS can add a third.
#[cfg(cargo_config_flag)]
pub fn config_variant_active() -> &'static str {
    "cargo-config"
}

#[cfg(not(cargo_config_flag))]
pub fn config_variant_active() -> &'static str {
    "no-config"
}

#[cfg(target_config_flag)]
pub fn target_config_active() -> bool {
    true
}

#[cfg(not(target_config_flag))]
pub fn target_config_active() -> bool {
    false
}

// RS-CAN-PROJ-021: cfg(test), cfg(doc), cfg(doctest) entities.
#[cfg(test)]
pub mod test_only {
    pub fn test_helper() -> u32 {
        42
    }
}

#[cfg(doc)]
pub struct DocOnly {
    pub value: u32,
}

#[cfg(doctest)]
pub fn doctest_only() -> &'static str {
    "doctest"
}

/// RS-CAN-PROJ-021: maps commands to compilation sets is documented in `coverage.md`.
/// This normal function is compiled under `cargo build`.
pub fn normal_api() -> u32 {
    1
}

// RS-CAN-PROJ-005 / RS-CAN-PROJ-022: `normal-dep`'s target-role instance (no
// `host-only` feature), compiled alongside its host-role instance linked by
// `build.rs`. Same source, same version, two simultaneous crate instances.
pub fn normal_dep_role() -> &'static str {
    normal_dep::role()
}

// RS-CAN-PROJ-001: package vs target vs crate identity.
// This type exists in the library crate. The binary crate `cargo-build-model-bin`
// re-uses the same source via `mod shared_identity` vs external crate import,
// producing two distinct `SharedType` identities that do not unify.
//
// Demonstration: `src/shared_identity.rs` is compiled as `cargo_build_model::SharedType`
// and as `cargo_build_model_bin::SharedType`; the types are distinct.
pub mod shared_identity;

// RS-CAN-PROJ-022: fine-grained build identity.
// The same `build_identity` source produces different cfg-gated API under different
// feature/profile/cfg. `build_identity::variant()` returns a different string per
// compilation variant.

// RS-CAN-PROJ-015: profile-observable differences.
pub use profile_observables::{
    debug_assertions_enabled, opt_level_observable, overflow_demo, panic_strategy,
};

// RS-CAN-PROJ-002: cfg-disabled subtree.
// `disabled_mod` is only compiled when its cfg is satisfied; otherwise absent.
#[cfg(any())]
pub mod disabled_subtree {
    pub fn never_compiled() {}
}

// Counterexamples documented beside valid demonstrations:
// - Duplicate target names would fail: defining two `[[bin]] name = "cargo-build-model-bin"`
//   is rejected by Cargo as duplicate target.
// - Missing inherited key: omitting `license.workspace = true` where required emits
//   `error: missing inherited key `package.license``.
// - Library reaching a dev dependency: `cargo_build_model` cannot `use dev_dep::*`
//   because dev-dependencies are not in the normal graph; such an import fails.
// - Unused-patch warning: a `[patch.crates-io]` entry for a package not in the graph
//   emits `warning: patch for 'unused-crate' in ... was not used`.
// - Registry-spelled identifier: using `hyphen-crate` (with hyphen) as a Rust path,
//   e.g. `use hyphen-crate::Foo`, fails to parse (`-` is not valid in a path
//   segment); the dependency-key alias `use hyphen_v2::Foo` is required instead.
