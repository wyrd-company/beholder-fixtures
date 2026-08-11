//! RS-CAN-PROJ-002: integration test target.
//! Explicit `[[test]] path = "tests/integration_test.rs"` (conventional would be auto-discovered).
//! This file demonstrates the test target existence. The `cargo test` command
//! compiles this target; it contains no `#[test]` functions so the single
//! planned unit test in `src/test_cfg.rs` remains the only test.

use cargo_build_model::normal_api;

#[allow(dead_code)]
fn integration_helper() -> u32 {
    normal_api()
}
