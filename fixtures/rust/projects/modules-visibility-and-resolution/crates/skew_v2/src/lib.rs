//! Skew crate version 0.2.0 - same package name as skew_v1, different version.

pub struct SkewType {
    pub version: &'static str,
}

impl SkewType {
    pub fn new() -> Self {
        Self { version: "0.2.0" }
    }
}

pub fn skew_version() -> &'static str {
    "0.2.0"
}

pub const SKEW_CONST: u32 = 2;
