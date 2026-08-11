//! Stable standard lazy globals and one legacy macro-backed case.

use std::collections::BTreeMap;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{LazyLock, OnceLock};

use lazy_static::lazy_static;

use crate::core::{CatalogItem, CatalogKind, Token};

/// Shared configuration initialized once through `OnceLock`.
static SHARED_CONFIG: OnceLock<BTreeMap<&'static str, u32>> = OnceLock::new();

/// Registry bootstrapped lazily through `LazyLock`.
static SHARED_REGISTRY: LazyLock<Vec<CatalogItem>> = LazyLock::new(|| {
    vec![
        CatalogItem::new(Token::new(1), CatalogKind::Primary, "alpha"),
        CatalogItem::new(Token::new(2), CatalogKind::Secondary, "beta"),
    ]
});

lazy_static! {
    /// Legacy macro-generated lazy static referenced through ordinary syntax.
    static ref LEGACY_COUNTER: AtomicUsize = AtomicUsize::new(0);
}

/// Access the once-initialized configuration map.
pub fn shared_config() -> &'static BTreeMap<&'static str, u32> {
    SHARED_CONFIG.get_or_init(|| {
        let mut map = BTreeMap::new();
        map.insert("window", 30);
        map.insert("retries", 3);
        map
    })
}

/// Access the lazily initialized registry.
pub fn shared_registry() -> &'static [CatalogItem] {
    SHARED_REGISTRY.as_slice()
}

/// Read the legacy counter through the macro-generated hidden wrapper.
pub fn legacy_counter_value() -> usize {
    LEGACY_COUNTER.load(Ordering::Relaxed)
}

/// Bump the legacy counter to exercise hidden `Deref` behavior.
pub fn bump_legacy_counter() -> usize {
    LEGACY_COUNTER.fetch_add(1, Ordering::Relaxed) + 1
}

/// Summarize all lazy global surfaces.
pub fn lazy_global_summary() -> String {
    let config = shared_config();
    let registry_len = shared_registry().len();
    let counter = legacy_counter_value();
    format!(
        "config_keys={}:registry_len={}:legacy_counter={}",
        config.len(),
        registry_len,
        counter
    )
}
