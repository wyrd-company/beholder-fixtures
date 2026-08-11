//! Consumer iterating the collected set — RS-CAN-ECO-007.

use crate::registration::{PluginDescriptor, iter_plugins};

/// Collect the set and format as sorted names.
pub fn consumer_descriptor_summary() -> String {
    let mut names: Vec<&'static str> = iter_plugins().into_iter().map(|d| d.name).collect();
    names.sort_unstable();
    names.join(",")
}

/// Return the number of registered plugins.
pub fn plugin_count() -> usize {
    iter_plugins().len()
}

/// Return references to all registered descriptors.
pub fn collected_descriptors() -> Vec<&'static PluginDescriptor> {
    iter_plugins()
}

/// True if no producer was linked — demonstrates the dead/unlinked omission:
/// if a producer's object file is not linked (or is eliminated by link-time
/// dead code elimination), its submission never appears in `inventory::iter`.
pub fn has_any_plugin() -> bool {
    plugin_count() > 0
}
