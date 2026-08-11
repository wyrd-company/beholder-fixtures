// Shared source file mounted at multiple module paths.
// Each mount creates a distinct nominal type identity.

pub struct SharedMarker {
    pub id: u32,
}

impl SharedMarker {
    pub fn new(id: u32) -> Self {
        Self { id }
    }

    pub fn describe(&self) -> &'static str {
        "shared"
    }
}

pub fn shared_fn() -> u32 {
    42
}

pub const SHARED_CONST: u32 = 100;
