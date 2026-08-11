//! Blanket extension trait adding methods to every sealed catalog entry.

use crate::sealed::CatalogEntry;

/// Extension methods available to all catalog entries through a blanket impl.
pub trait CatalogExt: CatalogEntry {
    /// Format the entry label with a stable prefix.
    fn formatted_label(&self) -> String {
        format!("[catalog] {}", self.label())
    }

    /// Report whether the label is non-empty.
    fn has_label(&self) -> bool {
        !self.label().is_empty()
    }
}

impl<T: CatalogEntry> CatalogExt for T {}
