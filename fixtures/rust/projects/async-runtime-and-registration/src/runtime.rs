//! Runtime attribute macros — source vs compiled shape (RS-CAN-ECO-003).
//!
//! `tokio::main` and `tokio::test` are attribute macros that rewrite an `async`
//! function into a synchronous wrapper that builds and drives a runtime, moves
//! the body into a future, and preserves the original signature for callers.
//! The source spelling is `async fn` with an attribute; the compiled shape is a
//! generated `fn main()` / `fn test()` that constructs a `Runtime` and blocks
//! on the async body. This module keeps both the source form and the manual
//! equivalent visible.

use tokio::runtime::{Builder, Runtime};

/// Source form: runtime entry attribute rewrites this async main.
///
/// The attribute form is demonstrated in `src/bin/async_main.rs` as a binary
/// entry point. The library preserves the same shape as a function item so the
/// code graph can observe the attribute, the async body, and the wrapper
/// relationship without requiring the binary to be the test subject.
///
/// Compiled shape (documentation, pinned Tokio 1.47.1): the macro emits a
/// synchronous `fn main()` containing a local `async move` body passed to
/// `Builder::new_multi_thread().enable_all().build().unwrap().block_on`,
/// with no hidden module.
pub async fn entry_point_body() -> u32 {
    // Body that would be wrapped by `#[tokio::main]`.
    42
}

/// Manually expanded equivalent of `#[tokio::main] async fn main()`.
/// Demonstrates the compiled semantic shape beside the attribute source.
pub fn manual_runtime_entry() -> u32 {
    let rt = build_multi_thread_runtime();
    rt.block_on(entry_point_body())
}

/// Build a current-thread runtime (single-threaded flavor).
pub fn build_current_thread_runtime() -> Runtime {
    Builder::new_current_thread()
        .enable_all()
        .build()
        .expect("current-thread runtime builds")
}

/// Build a multi-thread runtime gated by the `rt-multi-thread` feature.
///
/// The dependency-feature-gated context selects the multi-thread flavor via
/// the crate feature `rt-multi-thread` / `full-runtime` which forwards to
/// `tokio/rt-multi-thread`. The `#[cfg]` keeps each referenced `Builder`
/// API valid in the context where it is compiled.
#[cfg(feature = "rt-multi-thread")]
pub fn build_multi_thread_runtime() -> Runtime {
    Builder::new_multi_thread()
        .enable_all()
        .build()
        .expect("multi-thread runtime builds")
}

#[cfg(not(feature = "rt-multi-thread"))]
pub fn build_multi_thread_runtime() -> Runtime {
    // Fallback that keeps the symbol present for the code graph in the
    // default context where `rt-multi-thread` is not enabled. The fallback
    // uses the always-available current-thread builder so the crate still
    // compiles offline without the extra dependency feature.
    Builder::new_current_thread()
        .enable_all()
        .build()
        .expect("fallback runtime builds")
}

/// Demonstrates granular runtime feature gating and spawn requirements.
///
/// `tokio::spawn` requires `Send + 'static`; local tasks via `task::LocalSet`
/// relax `Send` at the cost of `!Send` confinement.
pub async fn spawn_demo() -> u32 {
    // Spawned future must be Send + 'static.
    let handle = tokio::spawn(async { 21u32 });
    let from_spawn = handle.await.expect("spawned task joins");

    // Local, non-Send task via LocalSet.
    let from_local = tokio::task::LocalSet::new()
        .run_until(async {
            let local = tokio::task::spawn_local(async { 21u32 });
            local.await.expect("local task joins")
        })
        .await;

    from_spawn + from_local
}

/// Whether the feature-gated multi-thread context is active.
///
/// Compile-time probe used by `runtime_feature_summary`. The flag reflects the
/// crate feature `rt-multi-thread` / `full-runtime` which forwards to
/// `tokio/rt-multi-thread` (visible in `cargo tree`).
#[cfg(feature = "rt-multi-thread")]
pub const RT_MULTI_THREAD_ENABLED: bool = true;
#[cfg(not(feature = "rt-multi-thread"))]
pub const RT_MULTI_THREAD_ENABLED: bool = false;

/// Summary that exercises both runtime flavors.
pub fn runtime_summary() -> String {
    // Exercise both builder paths without running them to keep graph edges.
    let _ = build_current_thread_runtime();
    let _ = build_multi_thread_runtime();
    format!("rt:multi_thread={RT_MULTI_THREAD_ENABLED}")
}

/// Extended summary that records the dependency-feature-gated context.
pub fn runtime_feature_summary() -> String {
    if RT_MULTI_THREAD_ENABLED {
        "feature:rt-multi-thread".to_owned()
    } else {
        "feature:default-rt".to_owned()
    }
}

/// The rewritten entry for tests — only exists under `cargo test`.
///
/// The source is `#[tokio::test] async fn test_entry_async_adds()` stacked
/// with `#[tracing::instrument]` on the same item to demonstrate macro
/// stacking; the compiled shape is a synchronous `#[test] fn` that builds a
/// runtime and enters an `INFO` span (`tracing::span!(Level::INFO, …)`).
/// This single planned test supplies the test-attribute portion of
/// RS-CAN-ECO-003. The wrapper body only compiles under the test harness.
#[cfg(test)]
#[tracing::instrument]
#[tokio::test(flavor = "current_thread")]
async fn test_entry_async_adds() {
    // Body wrapped by `#[tokio::test]` — runs inside a runtime in the test
    // compilation. Source: `async fn`; compiled: generated `fn` + `Runtime::block_on`.
    let value = entry_point_body().await;
    assert_eq!(value, 42);
}
