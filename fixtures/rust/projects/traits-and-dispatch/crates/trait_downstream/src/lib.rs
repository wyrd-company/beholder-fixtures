//! Cross-crate boundary for coherence, orphan, and conversion effects.

/// Local trait defined in downstream crate.
pub trait DownstreamTrait {
    fn downstream_name(&self) -> &'static str;
}

/// Local type in downstream crate.
pub struct DownstreamType(pub i32);

impl DownstreamTrait for DownstreamType {
    fn downstream_name(&self) -> &'static str {
        "DownstreamType via DownstreamTrait"
    }
}

/// Demonstrates that downstream can consume types/traits from upstream
/// via path dependencies when this crate is used as a workspace member.
/// This crate itself has no dependencies to keep the boundary minimal,
/// but the workspace relationship proves the cross-crate compilation context.
pub fn downstream_summary() -> String {
    let dt = DownstreamType(7);
    dt.downstream_name().to_owned()
}

/// Conversion helper in downstream crate.
pub struct DownstreamId(pub u32);

impl From<u32> for DownstreamId {
    fn from(v: u32) -> Self {
        Self(v)
    }
}

/// Valid cross-crate conversion using local From impl.
pub fn downstream_from_demo(value: u32) -> DownstreamId {
    DownstreamId::from(value)
}
