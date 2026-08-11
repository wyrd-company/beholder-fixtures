//! Cross-crate consumer for facade identity and sealed-trait effects.

use api_facades_and_lazy_globals::core::{CatalogItem, core_summary};
use api_facades_and_lazy_globals::extension::CatalogExt;
use api_facades_and_lazy_globals::facade::{Token, facade_summary};
use api_facades_and_lazy_globals::prelude::*;
use api_facades_and_lazy_globals::wrappers::{RecordId, RecordView, wrapper_summary};
use api_facades_and_lazy_globals::{CatalogKind, fixture_summary, lazy_global_summary};

/// Prove facade and core paths refer to the same `Token` identity.
pub fn cross_crate_identity(item: &CatalogItem) -> (String, String, bool) {
    let core_path = core_summary(item);
    let facade_path = facade_summary(item);
    let same_type = std::any::TypeId::of::<api_facades_and_lazy_globals::core::Token>()
        == std::any::TypeId::of::<Token>();
    (core_path, facade_path, same_type)
}

/// Exercise the prelude glob and blanket extension trait from a downstream crate.
pub fn downstream_catalog_view(item: &CatalogItem) -> String {
    let _prelude_marker = PRELUDE_GLOB;
    let view = RecordView::new(RecordId::new(item.token().value().into()), item.token());
    format!("{}:{}", item.formatted_label(), wrapper_summary(&view))
}

/// Summarize downstream consumption of facade, sealed, and lazy surfaces.
pub fn downstream_summary() -> String {
    let item = CatalogItem::new(Token::new(9), CatalogKind::Primary, "downstream");
    let (core_path, facade_path, same_type) = cross_crate_identity(&item);
    format!(
        "fixture={}:core={}:facade={}:same_token_type={}:lazy={}:view={}",
        fixture_summary(),
        core_path,
        facade_path,
        same_type,
        lazy_global_summary(),
        downstream_catalog_view(&item)
    )
}
