#![allow(dead_code)]

//! RS-CAN-PROJ-003: distinct package, library, executable, and dependency-key names.
//! Package name is `hyphen-crate` (hyphen), library is `hyphen_crate_lib` (underscore mapping),
//! executable is `hyphen-executable`, dependency key in consumer is `hyphen_v2`/`hyphen_v3`.

pub struct HyphenType(pub u32);

pub fn library_fn() -> HyphenType {
    HyphenType(200)
}

// Two versions under aliases: this is v0.2.0; v0.3.0 is in hyphen-crate-v03.
pub const VERSION: &str = "0.2.0";

/// Demonstrates `package =` vs local name: consumer writes
/// `hyphen_v2 = { package = "hyphen-crate", path = "...v02" }`
/// and then `use hyphen_crate_lib::HyphenType` (library name) and `hyphen_v2` (key) for manifest.
pub fn via_package_name() -> HyphenType {
    HyphenType(202)
}
