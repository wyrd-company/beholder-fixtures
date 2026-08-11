//! Producer in a separate module — RS-CAN-ECO-007.

use crate::registration::PluginDescriptor;

/// Descriptor produced by module `producer_beta`.
pub const PLUGIN_BETA_NAME: &str = "beta";
pub const PLUGIN_BETA_VERSION: u32 = 2;

inventory::submit! {
    PluginDescriptor {
        name: "beta",
        version: 2,
    }
}

/// Local helper for the beta producer.
pub fn beta_helper() -> &'static str {
    PLUGIN_BETA_NAME
}
