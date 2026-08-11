//! Explicit binary target for RS-CAN-PROJ-002.
//! Conventional path would be `src/main.rs` for the primary package; here we use
//! explicit `[[bin]] path = "src/bin/secondary.rs"` to demonstrate explicit mounting.

fn main() {
    println!("secondary binary");
}
