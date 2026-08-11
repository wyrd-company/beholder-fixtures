// Shared source for dual include/module mounting demonstration (RS-CAN-PROJ-012).
// This file is intentionally mounted both as a module and included via `include!`
// to demonstrate distinct nominal types.

pub struct DualType(pub u32);

impl DualType {
    pub fn value(&self) -> u32 {
        self.0
    }
}

pub const DUAL_HANDWRITTEN_CONST: u32 = 101;

pub fn dual_handwritten_fn() -> u32 {
    101
}
