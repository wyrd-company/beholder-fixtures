//! RS-CAN-PROJ-001 and RS-CAN-PROJ-002: binary target.
//! Conventional free-standing binary (`src/bin/*.rs`) plus explicit path in Cargo.toml.

// RS-CAN-PROJ-001: one source compiled under two crate identities.
// Mount the same file as a local module (distinct crate identity) vs external crate.
#[path = "../shared_identity.rs"]
mod local_shared;

use cargo_build_model::shared_identity::SharedType as ExternalShared;
use local_shared::SharedType as LocalShared;

fn takes_external(_: ExternalShared) {}
fn takes_local(_: LocalShared) {}

fn main() {
    let ext = ExternalShared(1);
    let loc = LocalShared(2);

    // These are distinct types; the following would fail if uncommented:
    // takes_external(loc);
    // takes_local(ext);

    // Prevent unused warnings
    let _ = ext.value();
    let _ = loc.value();

    // RS-CAN-PROJ-005: build-script host/target reporting is observable via env at build time.
    // RS-CAN-PROJ-005 / RS-CAN-PROJ-022: normal-dep's target-role instance.
    // RS-CAN-PROJ-015: profile observables, real per-profile behavior.
    println!(
        "cargo-build-model-bin: external={}, local={}, normal_dep_role={}, debug_assertions={}, panic_strategy={}, opt_level={}",
        ext.value(),
        loc.value(),
        cargo_build_model::normal_dep_role(),
        cargo_build_model::profile_observables::debug_assertions_enabled(),
        cargo_build_model::profile_observables::panic_strategy(),
        cargo_build_model::profile_observables::opt_level_observable(),
    );
}
