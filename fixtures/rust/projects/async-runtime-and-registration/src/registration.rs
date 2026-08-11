//! Link-time registration via linker sections (RS-CAN-ECO-007).
//!
//! `inventory` collects distributed values through platform linker sections
//! without direct source references. Each producer submits a value with
//! `inventory::submit!`; the consumer iterates with `inventory::iter`. The
//! host ELF linker sections used by the registration crate provide the
//! collection mechanism; unlinked or dead-code-eliminated producers disappear
//! from the iteration.

/// Descriptor collected by the registration crate.
#[derive(Debug, PartialEq, Eq, Clone)]
pub struct PluginDescriptor {
    /// Stable identifier for the plugin.
    pub name: &'static str,
    /// Plugin version within the fixture.
    pub version: u32,
}

// The collection point — no direct references to producers appear here.
inventory::collect!(PluginDescriptor);

pub mod consumer;
pub mod producer_alpha;
pub mod producer_beta;

/// Iterate the collected set — the consumer side.
pub fn iter_plugins() -> Vec<&'static PluginDescriptor> {
    inventory::iter::<PluginDescriptor>.into_iter().collect()
}

/// All plugin descriptors registered from separate modules.
pub fn all_plugins() -> Vec<&'static PluginDescriptor> {
    iter_plugins()
}

/// Name list of all plugins (deterministic ordering is not guaranteed by
/// `inventory`; callers sort if they need stability — fixture collects set
/// semantics, not order).
pub fn all_plugin_names() -> Vec<&'static str> {
    let mut names: Vec<&'static str> = iter_plugins().into_iter().map(|p| p.name).collect();
    names.sort_unstable();
    names
}

/// Consumer summary that exercises iteration over the collected set.
pub fn consumer_summary() -> String {
    let plugins = iter_plugins();
    format!("plugins:{}", plugins.len())
}

/// Combined registration summary.
pub fn registration_summary() -> String {
    format!("registration:{}", consumer::consumer_descriptor_summary())
}
