//! Transitive dependency crate - not directly depended by root crate.

/// Type that is unnameable from root without re-export.
pub struct TransitiveType {
    pub value: u32,
}

impl TransitiveType {
    pub fn new(v: u32) -> Self {
        Self { value: v }
    }
}

/// Marker for transitive version identity.
pub fn transitive_origin() -> &'static str {
    "fixture-transitive 0.1.0"
}
