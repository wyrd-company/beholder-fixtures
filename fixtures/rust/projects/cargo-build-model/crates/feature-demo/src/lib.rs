#![allow(dead_code)]

//! RS-CAN-PROJ-006: Cargo features, optional dependencies, and forwarding.
//! Demonstrates default, non-default, optional-dependency, `dep:`, strong- and
//! weak-forwarded, all-features, and no-default-features builds,
//! plus feature-gated API and impls.

#[cfg(feature = "feat-a")]
pub fn feat_a_api() -> &'static str {
    "feat-a-enabled"
}

#[cfg(not(feature = "feat-a"))]
pub fn feat_a_api() -> &'static str {
    "feat-a-disabled"
}

#[cfg(feature = "feat-b")]
pub fn feat_b_api() -> u32 {
    2
}

#[cfg(feature = "feat-c")]
pub struct FeatCType(pub u32);

#[cfg(feature = "optional-bridge")]
pub fn optional_api() -> u32 {
    optional_dep_crate::optional_fn()
}

// Implicit optional feature: `implicit-optional-dep` has no `dep:` reference
// anywhere in this table, so its auto-created feature (same name as the
// dependency) is what gates this function.
#[cfg(feature = "implicit-optional-dep")]
pub fn implicit_optional_api() -> u32 {
    implicit_optional_dep::implicit_fn()
}

// dep: syntax: feature `use-optional` pulls in optional-dep-crate via `dep:`.
#[cfg(feature = "use-optional")]
pub fn use_optional_api() -> u32 {
    optional_dep_crate::optional_fn()
}

// Strong forwarding: always enables the dep's feature even if dep not otherwise enabled.
// Weak forwarding: `optional-dep-crate?/feat-a` only if optional-dep-crate already enabled.
#[cfg(feature = "strong-forward")]
pub fn strong_forward_api() -> &'static str {
    "strong"
}

#[cfg(feature = "weak-forward")]
pub fn weak_forward_api() -> &'static str {
    "weak"
}

pub fn always_api() -> u32 {
    1
}

// Feature-gated impl
pub struct GatedStruct(pub u32);

#[cfg(feature = "feat-b")]
impl GatedStruct {
    pub fn gated_method(&self) -> u32 {
        self.0 + 100
    }
}

#[cfg(not(feature = "feat-b"))]
impl GatedStruct {
    pub fn gated_method(&self) -> u32 {
        self.0
    }
}

// Forbidden combination compile_error! for RS-006 counterexample (documented, not active):
// If both feat-a and feat-b with extra constraint, we would emit compile_error!,
// but the fixture keeps a valid build; the counterexample is documented here:
// `#[cfg(all(feature = "feat-a", feature = "feat-b"))] compile_error!("feat-a and feat-b are mutually exclusive in this example")`
// Cargo does not make requested features mutually exclusive - this is the documented valid behavior.
