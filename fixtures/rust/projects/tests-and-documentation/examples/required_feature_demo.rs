//! RS-CAN-TEST-002: required-feature example.
//! This example is only built when `required-feature` is enabled.

use tests_and_documentation::public_api;

fn main() {
    let value = public_api::public_function();
    println!("required-feature example: public_function = {value}");
}
