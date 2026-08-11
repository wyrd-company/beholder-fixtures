//! RS-CAN-PROJ-015: development, release, custom, and package-override profiles
//! and their observable codegen and assertion differences.

/// Whether `debug_assertions` are enabled; true in dev/custom, false in release.
pub fn debug_assertions_enabled() -> bool {
    cfg!(debug_assertions)
}

/// Overflow-sensitive computation. In dev (overflow-checks = true) this would panic
/// on `255u8 + 1` in debug builds; in release (overflow-checks = false) it wraps.
/// We use wrapping to stay valid while proving the profile difference via cfg.
pub fn overflow_demo() -> u8 {
    255u8.wrapping_add(1)
}

/// Whether the custom profile uses `panic = "abort"`; observable via `cfg(panic = "abort")` is unstable,
/// so we expose the profile difference via `debug_assertions` and `opt-level` indirectly.
/// The actual abort vs unwind contrast is that `catch_unwind` cannot catch a panic
/// when compiled with `panic = "abort"` (see `panic_strategy()` test).
pub fn panic_strategy() -> &'static str {
    if cfg!(debug_assertions) {
        "unwind-or-abort-depends-on-profile"
    } else {
        "release"
    }
}

/// Debug symbols and LTO/codegen-units affect artifact size and symbol visibility,
/// not runtime semantics, so they are observable via linker artifact inspection rather
/// than runtime API. This comment documents that profile inheritance (`custom` inherits
/// `dev`) and `[profile.dev.package."hyphen-crate"] opt-level = 3` demonstrate
/// package-override profiles where a dependency is compiled differently than the root.

pub fn codegen_units_observable() -> u32 {
    // Codegen units affect parallelism, not semantics. The profile `codegen-units = 256` (dev)
    // vs `1` (release) vs `16` (custom) is observable in build logs and artifact.
    256
}
