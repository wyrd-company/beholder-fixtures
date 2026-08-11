//! Core definitions consumed through both core and facade paths.

use crate::sealed::CatalogEntry;

/// Stable identity token re-exported by the facade module.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Token {
    value: u32,
}

impl Token {
    /// Construct a token from its numeric identity.
    pub const fn new(value: u32) -> Self {
        Self { value }
    }

    /// Accessor without a `get_` prefix.
    pub const fn value(self) -> u32 {
        self.value
    }
}

/// Kind label for catalog entries.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum CatalogKind {
    /// Primary entry kind.
    Primary,
    /// Secondary entry kind.
    Secondary,
}

/// Core catalog item implementing the sealed entry trait.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct CatalogItem {
    token: Token,
    kind: CatalogKind,
    label: String,
}

impl CatalogItem {
    /// Build a catalog item from its parts.
    pub fn new(token: Token, kind: CatalogKind, label: impl Into<String>) -> Self {
        Self {
            token,
            kind,
            label: label.into(),
        }
    }

    /// Borrowed view of the backing token.
    pub fn token(&self) -> Token {
        self.token
    }

    /// Borrowed kind accessor.
    pub fn kind(&self) -> CatalogKind {
        self.kind
    }
}

impl CatalogEntry for CatalogItem {
    fn label(&self) -> &str {
        &self.label
    }
}

/// Summary of core-path identity.
pub fn core_summary(item: &CatalogItem) -> String {
    format!("core:{}:{}", item.token().value(), item.label())
}
