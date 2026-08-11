//! RS-CAN-TRAIT-002 — coherence, orphan coverage, and overlap.

/// Local trait that can be implemented for foreign types.
pub trait LocalTrait {
    fn local_name(&self) -> &'static str;
}

/// Local nominal type.
pub struct LocalType(pub i32);

/// Newtype workaround for foreign trait on foreign type.
pub struct Wrapper(pub Vec<i32>);

/// Local trait for foreign type (allowed: trait is local).
impl LocalTrait for String {
    fn local_name(&self) -> &'static str {
        "String via LocalTrait"
    }
}

/// Local trait for fundamental box wrapping a local type.
impl LocalTrait for Box<LocalType> {
    fn local_name(&self) -> &'static str {
        "Box<LocalType> via LocalTrait"
    }
}

/// Local trait for reference to local type (reference is fundamental).
impl LocalTrait for &LocalType {
    fn local_name(&self) -> &'static str {
        "&LocalType via LocalTrait"
    }
}

/// Foreign trait for local type (allowed: type is local).
impl std::fmt::Display for LocalType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "LocalType({})", self.0)
    }
}

/// Foreign trait for local wrapper (allowed).
impl std::fmt::Display for Wrapper {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Wrapper({:?})", self.0)
    }
}

/// Local trait for local type (trivial valid impl).
impl LocalTrait for LocalType {
    fn local_name(&self) -> &'static str {
        "LocalType via LocalTrait"
    }
}

/// Covered generic wrapper: local type appears inside Vec.
impl LocalTrait for Vec<LocalType> {
    fn local_name(&self) -> &'static str {
        "Vec<LocalType> via LocalTrait"
    }
}

pub fn coherence_summary() -> Vec<&'static str> {
    let s = String::from("hello");
    let lt = LocalType(1);
    let lt_ref: &LocalType = &lt;
    vec![
        s.local_name(),
        Box::new(LocalType(2)).local_name(),
        lt_ref.local_name(),
        LocalType(3).local_name(),
        Vec::<LocalType>::new().local_name(),
    ]
}

pub fn display_summary() -> String {
    format!("{} and {}", LocalType(10), Wrapper(vec![1, 2]))
}

/// Cross-crate coherence: local trait for downstream type (type is foreign from this crate's view
/// but local to the workspace). Demonstrates orphan coverage across crate boundary.
impl LocalTrait for trait_downstream::DownstreamType {
    fn local_name(&self) -> &'static str {
        "DownstreamType via LocalTrait (cross-crate)"
    }
}

/// Foreign trait (downstream) for local type.
impl trait_downstream::DownstreamTrait for LocalType {
    fn downstream_name(&self) -> &'static str {
        "LocalType via DownstreamTrait (cross-crate)"
    }
}

pub fn cross_crate_coherence_demo() -> String {
    let dt = trait_downstream::DownstreamType(3);
    let lt = LocalType(4);
    let via_local = LocalTrait::local_name(&dt);
    let via_downstream = trait_downstream::DownstreamTrait::downstream_name(&lt);
    format!("{via_local}|{via_downstream}")
}
