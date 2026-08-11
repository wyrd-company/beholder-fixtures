//! RS-CAN-PROJ-002: example target.
//! Conventional `examples/*.rs` plus explicit `[[example]] path` demonstrates target discovery.

use cargo_build_model::normal_api;

fn main() {
    let v = normal_api();
    println!("example: normal_api = {}", v);
}
