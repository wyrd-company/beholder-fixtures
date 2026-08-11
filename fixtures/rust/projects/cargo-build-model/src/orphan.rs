//! RS-CAN-PROJ-002: orphan file.
//! This file is not mounted by any `mod` declaration, target path, or `include!`.
//! It exists on disk but is not compiled. When linked via `#[path = "orphan.rs"]` it would
//! fail due to intentionally invalid syntax below, but as an orphan it causes no failure.

// This file is intentionally not referenced anywhere. If it were mounted, the following
// intentionally invalid item would cause a compilation error, demonstrating orphan detection.
// The valid fixture keeps this file unmounted, so `cargo build` succeeds.
// invalid syntax placeholder: this comment explains the counterexample.
