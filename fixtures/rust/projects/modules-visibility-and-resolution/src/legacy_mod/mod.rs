//! `name/mod.rs` legacy file mapping form.

pub fn legacy_fn() -> u32 {
    30
}

pub struct LegacyType {
    pub v: u32,
}

// Nested child resolved as `legacy_mod/inner.rs` via legacy convention.
pub mod inner;
