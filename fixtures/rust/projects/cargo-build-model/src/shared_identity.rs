/// RS-CAN-PROJ-001: one source file compiled under two crate identities.
/// This file is `src/shared_identity.rs`. It is compiled as part of the library crate
/// (`cargo_build_model`) and separately as part of the binary crate
/// `cargo-build-model-bin` via `#[path = "../shared_identity.rs"] mod`.
/// The two `SharedType` definitions are distinct nominal types despite identical source.

pub struct SharedType(pub u32);

impl SharedType {
    pub fn value(&self) -> u32 {
        self.0
    }
}

pub fn shared_fn() -> SharedType {
    SharedType(99)
}
