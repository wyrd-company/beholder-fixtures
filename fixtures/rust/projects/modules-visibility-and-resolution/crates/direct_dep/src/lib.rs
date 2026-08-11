//! Direct dependency crate - nameable via extern prelude.

pub use fixture_transitive::TransitiveType;

/// Direct type exposed and re-exported by root.
pub struct DirectType {
    pub value: u32,
}

impl DirectType {
    pub fn new(v: u32) -> Self {
        Self { value: v }
    }
}

/// Re-exported transitive type path demonstration.
pub type ReexportedTransitive = TransitiveType;

/// Macro exported for macro_use prelude demonstration (legacy).
#[macro_export]
macro_rules! direct_macro {
    () => {
        42
    };
}

pub fn direct_origin() -> &'static str {
    "fixture-direct 0.1.0"
}

pub use fixture_skew::SKEW_CONST as TRANSITIVE_SKEW_CONST;
/// Transitive skew re-export: fixture-skew 0.1.0 via direct dep
pub use fixture_skew::SkewType as TransitiveSkewType;

/// Value used in glob and re-export tests.
pub const DIRECT_CONST: u32 = 99;
