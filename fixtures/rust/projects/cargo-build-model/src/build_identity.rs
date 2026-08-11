//! RS-CAN-PROJ-022: fine-grained build identity.
//! One source producing multiple crate instances by role, feature, or version.
//! `variant()` returns different values depending on features, cfg, and crate instance.
//! Name and version alone do not identify a crate compilation.

#[cfg(feature = "extra")]
pub fn variant() -> &'static str {
    "feature_extra"
}

#[cfg(not(feature = "extra"))]
pub fn variant() -> &'static str {
    "feature_default"
}

/// Source-identical crate instances with different cfg APIs (host vs target, feature vs no-feature)
/// should not be considered identical by mangled symbol or path alone.
pub struct SourceIdenticalType(pub u32);

impl SourceIdenticalType {
    pub fn id(&self) -> u32 {
        self.0
    }
}
