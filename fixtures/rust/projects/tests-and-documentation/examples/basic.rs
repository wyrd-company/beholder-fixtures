//! RS-CAN-TEST-002: standard example target.

use tests_and_documentation::public_api;

fn main() {
    let value = public_api::public_function();
    println!("basic example: public_function = {value}");
}
