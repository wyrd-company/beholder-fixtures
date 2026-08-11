//! Fixture for Rust test and documentation compilation model.
//! Covers RS-CAN-TEST-001, RS-CAN-TEST-002, RS-CAN-TEST-003.

#![doc = include_str!("../README.md")]

pub mod docs;
pub mod harness;
pub mod private_api;
pub mod public_api;

pub use public_api::{PublicType, public_function};

/// Crate summary combining public API surface.
pub fn fixture_summary() -> u32 {
    let helper = private_api::private_helper();
    let const_val = private_api::private_const_value();
    let typed = private_api::private_type_value(&private_api::PrivateType { value: helper });
    public_api::public_function() + const_val + typed
}

// RS-CAN-TEST-001: unit test accessing a private ancestor.
// This module is compiled as part of the library crate, so it can access
// `private_api::private_helper` which is not visible outside the crate.
#[cfg(test)]
mod unit_tests {
    use super::private_api::private_helper;

    #[test]
    fn unit_accesses_private_ancestor() {
        assert_eq!(private_helper(), 7);
        assert_eq!(super::private_api::private_const_value(), 7);
    }

    #[test]
    fn unit_accesses_private_type() {
        let item = super::private_api::PrivateType { value: 9 };
        assert_eq!(item.value, 9);
    }
}

// RS-CAN-TEST-002: harness attributes and generated main coverage.
// These tests use the default libtest harness; each function is registered
// via `#[test]` and executed by the generated main.
#[cfg(test)]
mod harness_tests {
    #[test]
    fn passing() {
        assert_eq!(2 + 2, 4);
    }

    #[test]
    #[ignore]
    fn ignored_demo() {
        // This test is compiled but not executed by default.
        // `cargo test` reports it as ignored; `cargo test -- --ignored` runs it.
        assert_eq!(1, 1);
    }

    #[test]
    #[should_panic(expected = "expected panic")]
    fn panics() {
        panic!("expected panic");
    }

    #[test]
    fn result_demo() -> Result<(), String> {
        if true {
            Ok(())
        } else {
            Err("failure".to_string())
        }
    }
}

// RS-CAN-TEST-001 / RS-CAN-TEST-002: cfg(test) vs non-test lib variant.
// `test_only_flag` exists only when the crate is compiled with `cfg(test)`.
// Outside `cargo test`, this item is absent, demonstrating that `cfg(test)`
// is set on the crate under test and not on dependencies.
#[cfg(test)]
pub fn test_only_flag() -> bool {
    true
}

#[cfg(not(test))]
pub fn test_only_flag() -> bool {
    false
}

/// cfg doctest entity: present only during rustdoc doctest compilation.
#[cfg(doctest)]
pub fn doctest_only_helper() -> u32 {
    99
}
