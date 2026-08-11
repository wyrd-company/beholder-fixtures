//! Sealed trait restricting implementability to this crate.

mod private {
    /// Private supertrait marking which types may implement `CatalogEntry`.
    pub trait Sealed {}

    impl Sealed for crate::core::CatalogItem {}
}

/// Public catalog entry surface sealed against downstream implementations.
pub trait CatalogEntry: private::Sealed {
    /// Borrowed label accessor using idiomatic no-`get_` naming.
    fn label(&self) -> &str;
}
