//! Fixture demonstrating API facades, sealed traits, lazy globals, and naming
//! conventions for code-graph evaluation.

pub mod core;
pub mod extension;
pub mod facade;
pub mod lazy_globals;
pub mod naming;
pub mod prelude;
pub mod sealed;
pub mod wrappers;

pub use core::{CatalogItem, CatalogKind, Token};
pub use extension::CatalogExt;
pub use facade::facade_summary;
pub use lazy_globals::{lazy_global_summary, legacy_counter_value, shared_config, shared_registry};
pub use naming::{Label, Metric, naming_summary};
pub use sealed::CatalogEntry;
pub use wrappers::{RecordId, RecordView};

/// Project-level summary tying facade, lazy, and naming modules together.
pub fn fixture_summary() -> &'static str {
    "api-facades-and-lazy-globals"
}
