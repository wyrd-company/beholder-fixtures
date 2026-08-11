//! Fixture for runtime attribute macros and link-time registration.
//!
//! Demonstrates `RS-CAN-ECO-003` (tokio runtime entry / test attributes and
//! tracing instrumentation) and `RS-CAN-ECO-007` (inventory link-time
//! registration). Attribute macros rewrite source into wrappers, runtimes, and
//! spans; the registration crate collects distributed values via linker sections
//! without direct source references.

pub mod instrumentation;
pub mod registration;
pub mod runtime;

pub use instrumentation::{
    async_instrumented_work, instrumentation_summary, instrumented_add, instrumented_computation,
};
pub use registration::{
    PluginDescriptor, all_plugins, consumer_summary, iter_plugins, registration_summary,
};
pub use runtime::{
    build_current_thread_runtime, build_multi_thread_runtime, runtime_feature_summary,
    runtime_summary,
};

/// Aggregated summary tying fixture modules together.
pub fn fixture_summary() -> String {
    format!(
        "{}|{}|{}",
        runtime_summary(),
        instrumentation_summary(),
        registration_summary()
    )
}
