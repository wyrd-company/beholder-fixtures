//! Body-wrapping instrumentation attribute (RS-CAN-ECO-003).
//!
//! `#[tracing::instrument]` rewrites a function body into a wrapper that
//! creates a `Span`, enters it for the duration of the body, and records
//! arguments / return values according to the attribute's options. Source is a
//! plain function with an outer attribute; compiled shape is the same signature
//! calling `Span::enter` / `Span::in_scope` around the original block. Stacking
//! with the runtime attributes shows attribute composition order.

/// Instrumented synchronous function — body wrapped in a span.
///
/// Source: `#[tracing::instrument] fn instrumented_add(a, b) -> i32 { a + b }`
/// Compiled: span creation (`tracing::span!(Level::TRACE, "instrumented_add", a, b)`)
/// entered for the block, so every call appears as an instrumented event in a
/// span tree.
#[tracing::instrument]
pub fn instrumented_add(a: i32, b: i32) -> i32 {
    a + b
}

/// Instrumented function that skips an argument and records a custom field.
///
/// Demonstrates attribute options (`skip`, custom `fields`).
#[tracing::instrument(skip(secret), fields(result))]
pub fn instrumented_computation(value: i32, secret: &str) -> i32 {
    // `secret` is not recorded; `result` field is recorded via custom logic if desired.
    let _ = secret.len();
    value * 2
}

/// Instrumented async function — span is entered across await points.
///
/// The instrumentation wrapper must preserve `Send` / lifetime obligations of
/// the future it wraps; the span is held for the future's lifetime.
#[tracing::instrument]
pub async fn async_instrumented_work(value: i32) -> i32 {
    // Yield once so the future suspends while the span is active.
    tokio::task::yield_now().await;
    value + 1
}

/// Demonstrates stacking of runtime and instrumentation attributes.
///
/// The source has both `#[tokio::main]`-style runtime entry (shown canonically
/// in `src/bin/async_main.rs`) and `#[tracing::instrument]`; the compiled
/// shape is one wrapper inside the other. This function is not itself a runtime
/// entry to avoid multiple mains — the composition is documented and the
/// instrumentation wrapper remains valid when called from a runtime.
#[tracing::instrument]
pub async fn stacked_async_instrumented(value: i32) -> i32 {
    tokio::task::yield_now().await;
    value * 3
}

/// Demonstrates compile-time max-level filtering.
///
/// When `tracing` is built with `max_level_off` / `max_level_trace` feature
/// values (rarely exercised here), spans below the max level are elided at
/// compile time. This function remains valid regardless of the feature — the
/// elision is an additional compile-time variant preserved as documentation.
#[tracing::instrument(level = "debug")]
pub fn debug_level_instrumented(x: i32) -> i32 {
    x + 5
}

/// Exercises every instrumented item so the code graph observes call edges.
pub fn instrumentation_summary() -> i32 {
    let s = instrumented_add(2, 3);
    let t = instrumented_computation(10, "hidden");
    let u = debug_level_instrumented(1);
    s + t + u
}
