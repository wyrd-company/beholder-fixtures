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
    // RS-CAN-PROJ-015: profile observables
    let _ = cargo_build_model::profile_observables::debug_assertions_enabled();
    println!(
        "cargo-build-model-bin: external={}, local={}",
        ext.value(),
        loc.value()
    );
}
