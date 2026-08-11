//! Producer in a separate module — RS-CAN-ECO-007.

use crate::registration::PluginDescriptor;

/// Descriptor produced by module `producer_alpha`.
pub const PLUGIN_ALPHA_NAME: &str = "alpha";
pub const PLUGIN_ALPHA_VERSION: u32 = 1;

inventory::submit! {
    PluginDescriptor {
        name: "alpha",
        version: 1,
    }
}

/// Local helper showing the producer module has real items beyond the
/// registration.
pub fn alpha_helper() -> &'static str {
    PLUGIN_ALPHA_NAME
}
