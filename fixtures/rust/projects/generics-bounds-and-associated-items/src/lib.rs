//! Fixture demonstrating Rust generics, bounds, and associated items.

pub mod associated;
pub mod bounds;
pub mod const_generics;
pub mod elision;
pub mod gat;
pub mod generic_params;
pub mod precise_capture;
pub mod variance;

pub use associated::{Archive, Entry, Record, Transform};
pub use bounds::{Holder, Number};
pub use const_generics::{Buffer, Flag, Tag};
pub use elision::Document;
pub use gat::{Lending, Store};
pub use generic_params::{Inventory, Tagged};
pub use variance::{Owned, Shared};

/// Project-level summary tying all modules together.
pub fn fixture_summary() -> &'static str {
    "generics-bounds-and-associated-items"
}
