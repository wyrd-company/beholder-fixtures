//! RS-CAN-TEST-002: harness-less test target with explicit main.
//! `[[test]] harness = false` suppresses libtest collection; this binary provides its own entry point.

fn main() {
    let value = tests_and_documentation::public_api::public_function();
    assert_eq!(value, 42);
    // Explicit harness-less test passes by exiting 0.
    println!("harnessless test main: ok");
}
