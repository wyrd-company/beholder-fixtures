//! Fixture for RS-CAN-ECO-008 — target-gated Wasm bridge generator.
//!
//! Demonstrates `wasm-bindgen` as a bridge macro that creates a foreign-facing
//! surface and glue distinct from Rust `pub` and plain C exports. The macro
//! expands at host compile time (proc-macro) and produces wasm imports/exports
//! and ABI glue used only when linking for `wasm32-unknown-unknown`.

pub mod abi_adaptation;
pub mod bridge_exports;
pub mod bridge_imports;
pub mod ownership;
pub mod plain_exports;
pub mod wasm_target;

/// Aggregated entry touching each fixture area so `cargo build` and `cargo clippy`
/// observe reachable valid code for the code-graph fixture.
pub fn fixture_overview() -> &'static str {
    let _ = plain_exports::rust_visibility_anchor();
    let _ = plain_exports::c_exported_add(2, 3);
    let _ = bridge_exports::add(2, 3);
    let _ = bridge_exports::greet("fixture");
    let _ = bridge_exports::concat_strings("a".to_string(), "b".to_string());
    let _ = bridge_exports::create_buffer(4);
    let _ = bridge_exports::BridgeCounter::new(0);
    let _ = bridge_imports::imported_surface_label();
    let _ = ownership::ownership_label();
    let _ = abi_adaptation::abi_label();
    let _ = wasm_target::wasm_target_label();
    let _ = wasm_target::wasm_only_entry(42);
    "wasm-bindgen-bridge"
}
