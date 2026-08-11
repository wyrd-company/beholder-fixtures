//! RS-CAN-TEST-001: integration test crate seeing only public API.
//! Each file under `tests/*.rs` is a separate external crate.
//! This crate imports only public items and shared support.

use tests_and_documentation::public_api;

mod common;

#[test]
fn integration_sees_public_api() {
    assert_eq!(public_api::public_function(), 42);
    assert_eq!(public_api::PUBLIC_CONST, 42);
    common::shared_setup();
}

#[test]
fn integration_uses_public_type() {
    let item = public_api::public_type_demo();
    assert_eq!(item.value, 42);
    assert_eq!(common::shared_type_label(), "shared");
}
