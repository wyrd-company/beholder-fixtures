//! Prelude glob re-exporting the ergonomic entry surface.

pub use crate::core::{CatalogItem, CatalogKind, Token};
pub use crate::extension::CatalogExt;
pub use crate::naming::{Label, Metric};
pub use crate::sealed::CatalogEntry;
pub use crate::wrappers::{RecordId, RecordView};

/// Marker showing the prelude glob is the intended import surface.
pub const PRELUDE_GLOB: &str = "catalog_prelude";
