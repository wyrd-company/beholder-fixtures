//! Binary crate role mounting same file as library for RS-CAN-MOD-002.

// Same file `src/shared_source.rs` mounted in second crate role (binary) - distinct type identity.
#[path = "../shared_source.rs"]
pub mod bin_shared;

use modules_visibility_and_resolution::shared_first;

fn main() {
    let from_lib = shared_first::SharedMarker::new(10);
    let from_bin = bin_shared::SharedMarker::new(20);
    // Distinct types, same textual source - assignment between them would fail (documented).
    assert_eq!(from_lib.id, 10);
    assert_eq!(from_bin.id, 20);
    println!(
        "bin shared distinctness: lib {} bin {}",
        from_lib.id, from_bin.id
    );
}
