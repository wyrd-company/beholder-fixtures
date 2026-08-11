fn main() {
    // RS-CAN-PROJ-007: `unify_consumer_a` re-exports `unify_shared::active_features`.
    // Plain `cargo build` (no dev-deps) vs `cargo test --no-run` (dev-deps
    // included) observe different unified feature sets; see Cargo.toml.
    println!("resolver v1: {}", unify_consumer_a::active_features());
}
