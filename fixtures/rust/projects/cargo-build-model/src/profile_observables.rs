//! RS-CAN-PROJ-015: development, release, custom, and package-override profiles
//! and their observable codegen and assertion differences.

/// Whether `debug_assertions` are enabled; true in dev/custom, false in release.
pub fn debug_assertions_enabled() -> bool {
    cfg!(debug_assertions)
}

/// Overflow-sensitive computation using real (non-wrapping) addition, so the
/// profile's `overflow-checks` setting genuinely governs runtime behavior:
/// panics in dev/custom (`overflow-checks = true`) when called with an input
/// that overflows `u8`, wraps in release (`overflow-checks = false`).
pub fn overflow_demo(input: u8) -> u8 {
    input + 1
}

/// Real, stable `panic` cfg (RFC: `#[cfg(panic = "unwind")]` / `#[cfg(panic =
/// "abort")]`), reflecting the actual configured panic strategy: "abort" for
/// `[profile.custom] panic = "abort"`, "unwind" for dev/release (both
/// `panic = "unwind"`).
#[cfg(panic = "abort")]
pub fn panic_strategy() -> &'static str {
    "abort"
}

#[cfg(panic = "unwind")]
pub fn panic_strategy() -> &'static str {
    "unwind"
}

/// Real per-build `OPT_LEVEL`, forwarded by `build.rs` via
/// `cargo:rustc-env=CARGO_BUILD_MODEL_OPT_LEVEL=...` (Cargo does not expose
/// `opt-level` to source directly; a build script must relay it). Distinguishes
/// dev (`0`), release (`3`), and custom (`2`).
pub fn opt_level_observable() -> &'static str {
    env!("CARGO_BUILD_MODEL_OPT_LEVEL")
}

// `codegen-units`, LTO, and debug-symbol settings affect artifact size, symbol
// visibility, and link behavior, not any value observable from within compiled
// source, so they are documented rather than exposed as a runtime API here:
// `codegen-units = 256` (dev) vs `1` (release) vs `16` (custom) is observable
// via build logs/artifact inspection. Profile inheritance (`custom` inherits
// `dev`) and `[profile.dev.package."hyphen-crate"] opt-level = 3` demonstrate
// package-override profiles where a dependency is compiled differently than
// the root, independently verifiable the same way.
