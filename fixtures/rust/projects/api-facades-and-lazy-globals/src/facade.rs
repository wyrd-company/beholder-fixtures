//! Re-export facade controlling resolution and identity.

use crate::sealed::CatalogEntry;

pub use crate::core::{CatalogItem, CatalogKind, Token, core_summary};
pub use crate::wrappers::{RecordId, RecordView};

/// Consume the same `Token` type through the facade path.
pub fn facade_token_value(token: Token) -> u32 {
    token.value()
}

/// Summary proving facade and core paths share one type identity.
pub fn facade_summary(item: &CatalogItem) -> String {
    format!(
        "facade:{}:{}",
        facade_token_value(item.token()),
        item.label()
    )
}
