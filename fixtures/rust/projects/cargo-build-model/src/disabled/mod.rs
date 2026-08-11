//! RS-CAN-PROJ-002: cfg-disabled subtree.
//! This module is behind `#[cfg(feature = "never_enabled")]` and is normally not compiled.
//! It demonstrates a disabled subtree that exists on disk but contributes no Rust entity.

#[cfg(feature = "never_enabled")]
pub mod active {
    pub fn active_fn() -> u32 {
        7
    }
}

#[cfg(not(feature = "never_enabled"))]
pub fn disabled_placeholder() -> u32 {
    0
}
