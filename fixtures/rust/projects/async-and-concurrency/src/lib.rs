//! Fixture for Rust async and concurrency surface.
//! Covers RS-CAN-ASYNC-001 through RS-CAN-ASYNC-005 and RS-CAN-CONCUR-001 through RS-CAN-CONCUR-002.

pub mod async_closures;
pub mod async_fns_blocks;
pub mod atomics;
pub mod await_polling;
pub mod pinning;
pub mod sendability;
pub mod support;
pub mod threads;

/// Aggregated demonstration that touches each module so build and lint observe reachable valid code.
pub fn fixture_overview() -> &'static str {
    async_fns_blocks::drive_async_items();
    await_polling::await_polling_demo();
    pinning::pinning_demo();
    async_closures::async_closure_demo();
    sendability::sendability_demo();
    threads::threads_demo();
    atomics::atomics_demo();
    "async-and-concurrency"
}
