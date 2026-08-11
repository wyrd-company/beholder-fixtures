#![allow(unused)]

//! RS-CAN-PROJ-002: bench target.
//! Explicit `[[bench]] path = "benches/demo_bench.rs"` with `harness = false`.

fn bench_fn() -> u32 {
    cargo_build_model::normal_api()
}

fn main() {
    // Bench harness would call `bench_fn` repeatedly; we just demonstrate the target exists.
    let _ = bench_fn();
}
