//! RS-CAN-PROJ-006: implicit optional-dependency feature.
//! Depended on by `feature-demo` with `optional = true` and no `dep:` reference
//! anywhere in that crate's `[features]` table, so Cargo auto-creates a feature
//! of the same name (`implicit-optional-dep`) that enables this dependency.

pub fn implicit_fn() -> u32 {
    77
}
