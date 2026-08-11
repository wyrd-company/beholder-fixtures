//! RS-CAN-TEST-001: second integration target sharing the same support module.

use tests_and_documentation::public_api;

mod common;

#[test]
fn integration_second_target_public_api() {
    assert_eq!(public_api::public_function(), 42);
    common::shared_setup();
}

#[test]
fn integration_second_target_shared_value() {
    assert_eq!(common::shared_value(), 99);
    let item = public_api::PublicType::new(common::shared_type_label(), 1);
    assert_eq!(item.label, "shared");
}
