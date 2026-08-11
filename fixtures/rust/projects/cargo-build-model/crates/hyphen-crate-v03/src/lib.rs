#![allow(dead_code)]

//! RS-CAN-PROJ-003 and RS-CAN-PROJ-009: second version under alias (v0.3.0).

pub struct HyphenType(pub u32);

pub fn library_fn() -> HyphenType {
    HyphenType(300)
}

pub const VERSION: &str = "0.3.0";

pub fn via_package_name() -> HyphenType {
    HyphenType(303)
}
