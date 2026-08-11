//! Fixture demonstrating Rust ownership and borrowing.

pub mod binding_modes;
pub mod borrow_exclusivity;
pub mod call_traits;
pub mod closure_capture;
pub mod destructuring_assignment;
pub mod interior_mutability;
pub mod moves_partial_moves;
pub mod nll_two_phase;
pub mod patterns;
pub mod temporary_scopes;

pub use binding_modes::binding_modes_summary;
pub use borrow_exclusivity::borrow_exclusivity_summary;
pub use call_traits::call_traits_summary;
pub use closure_capture::closure_capture_summary;
pub use destructuring_assignment::destructuring_assignment_summary;
pub use interior_mutability::interior_mutability_summary;
pub use moves_partial_moves::moves_summary;
pub use nll_two_phase::nll_two_phase_summary;
pub use patterns::patterns_summary;
pub use temporary_scopes::temporary_scopes_summary;

/// Top-level summary tying ownership and borrowing modules together.
pub fn fixture_summary() -> &'static str {
    "ownership-and-borrowing"
}
