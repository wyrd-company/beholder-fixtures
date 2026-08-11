//! RS-CAN-TEST-002: harness-less bench target with explicit main.
//! `[[bench]] harness = false` avoids requiring a benchmark framework crate.

fn bench_fn() -> u32 {
    tests_and_documentation::public_api::public_function()
}

fn main() {
    // Bench harness would call `bench_fn` repeatedly; this demonstrates the target exists.
    let value = bench_fn();
    assert_eq!(value, 42);
    println!("bench harnessless main: ok");
}
