//! Skew crate version 0.1.0 - same package name as skew_v2, different version.

pub struct SkewType {
    pub version: &'static str,
}

impl SkewType {
    pub fn new() -> Self {
        Self { version: "0.1.0" }
    }
}

pub fn skew_version() -> &'static str {
    "0.1.0"
}

pub const SKEW_CONST: u32 = 1;
