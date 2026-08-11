//! Public API surface for RS-CAN-TEST-001.
//! Integration test crates see only this public surface.

/// Returns a stable public value used by integration tests and examples.
///
/// ```
/// assert_eq!(tests_and_documentation::public_api::public_function(), 42);
/// ```
pub fn public_function() -> u32 {
    42
}

/// Public constant visible to integration crates.
pub const PUBLIC_CONST: u32 = 42;

/// Public type with public fields.
#[derive(Debug, PartialEq, Eq)]
pub struct PublicType {
    pub label: &'static str,
    pub value: u32,
}

impl PublicType {
    /// Create a new public type.
    pub fn new(label: &'static str, value: u32) -> Self {
        Self { label, value }
    }
}

/// Returns a public type instance for integration tests.
pub fn public_type_demo() -> PublicType {
    PublicType::new("demo", 42)
}
