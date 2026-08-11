//! Shared support module for RS-CAN-TEST-001.
//! This module is not an integration test target itself (`tests/common/mod.rs`
//! is not auto-discovered as a test binary); it is compiled separately into each
//! integration test crate that includes it via `mod common;`.

/// Returns a stable shared value for integration tests.
pub fn shared_value() -> u32 {
    99
}

/// Shared assertion helper used by multiple integration targets.
pub fn shared_setup() {
    assert_eq!(shared_value(), 99);
}

/// Shared public type helper.
pub fn shared_type_label() -> &'static str {
    "shared"
}
