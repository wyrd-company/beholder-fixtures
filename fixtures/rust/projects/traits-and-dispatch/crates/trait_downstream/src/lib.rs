//! Cross-crate boundary for coherence, orphan, and conversion effects.
//! This downstream crate consumes the upstream `traits-and-dispatch` crate
//! to demonstrate downstream coherence, orphan, and conversion effects.

use traits_and_dispatch::coherence::{LocalTrait, LocalType};
use traits_and_dispatch::conversion::{CheckedId, ConversionError, UserId};

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

/// Downstream coherence: local trait for foreign upstream type
/// (foreign type is upstream `LocalType`, local trait is `DownstreamTrait`).
impl DownstreamTrait for LocalType {
    fn downstream_name(&self) -> &'static str {
        "LocalType via DownstreamTrait (cross-crate)"
    }
}

/// Downstream coherence: foreign upstream trait for local downstream type
/// (foreign trait is upstream `LocalTrait`, local type is `DownstreamType`).
impl LocalTrait for DownstreamType {
    fn local_name(&self) -> &'static str {
        "DownstreamType via LocalTrait (cross-crate)"
    }
}

/// Cross-crate conversion: `From` upstream type for downstream type
/// demonstrates downstream orphan conversion. `From` is foreign, `DownstreamType`
/// is local, so this impl is legal.
impl From<LocalType> for DownstreamType {
    fn from(value: LocalType) -> Self {
        Self(value.0)
    }
}

/// Cross-crate conversion: `From` upstream `UserId` for downstream `DownstreamId`.
impl From<UserId> for DownstreamId {
    fn from(value: UserId) -> Self {
        Self(value.0)
    }
}

/// Valid cross-crate coherence demonstration.
pub fn downstream_coherence_demo() -> String {
    let dt = DownstreamType(7);
    let lt = LocalType(4);
    let via_local = LocalTrait::local_name(&dt);
    let via_downstream = DownstreamTrait::downstream_name(&lt);
    format!("{via_local}|{via_downstream}")
}

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

/// Cross-crate conversion via `From` for upstream types.
pub fn downstream_cross_conversion_demo() -> String {
    let local = LocalType(5);
    let dt: DownstreamType = DownstreamType::from(local);
    let uid = UserId(9);
    let did: DownstreamId = DownstreamId::from(uid);
    let checked = CheckedId::try_from(10_i64).unwrap();
    let _ = ConversionError("demo".to_owned());
    format!("{}|{}|{:?}", dt.0, did.0, checked)
}
