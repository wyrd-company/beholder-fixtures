//! Crate edge for `cfg_attr` injection of `no_std` when `fixture_no_std_edge` is set.

#![cfg_attr(fixture_no_std_edge, no_std)]

#[cfg(fixture_no_std_edge)]
extern crate alloc;

/// Allocator identity selected by cfg-injected `no_std`.
pub fn allocator_label() -> &'static str {
    if cfg!(fixture_no_std_edge) {
        "no_std_edge"
    } else {
        "std_edge"
    }
}

/// Global allocator label for the active edge.
pub fn active_allocator_name() -> &'static str {
    if cfg!(fixture_no_std_edge) {
        "alloc::Global"
    } else {
        "std::alloc::System"
    }
}
