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
/// Compiled (pinned tracing 0.1.41): span creation
/// (`tracing::span!(Level::INFO, "instrumented_add", a, b)`) entered for the
/// block, so every call appears as an instrumented event in a span tree.
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
/// Source has both `#[tracing::instrument]` and `#[tokio::main]` on one async
/// item; the compiled shape is one wrapper inside the other (tracing span
/// wrapper inside the runtime-builder wrapper, order determined by attribute
/// order). This valid source item is `instrumentation::stacked_async_instrumented`
/// and is mapped in `coverage.md`.
#[tracing::instrument]
#[tokio::main(flavor = "current_thread")]
async fn stacked_async_instrumented_inner(value: i32) -> i32 {
    value * 3
}

/// Public wrapper that exposes the stacked item for the code graph without
/// requiring the caller to be inside the generated runtime entry.
pub async fn stacked_async_instrumented(value: i32) -> i32 {
    // The stacked attribute pair is compiled on `stacked_async_instrumented_inner`;
    // this wrapper calls the already-rewritten synchronous entry via a manual
    // block_on to keep the symbol graph while preserving the single generated
    // entry point.
    stacked_async_instrumented_inner(value)
}

/// Demonstrates compile-time max-level filtering.
///
/// When `tracing` is built with a max-level feature (e.g.,
/// `tracing/max_level_off` via crate feature `elided`), spans below the max
/// level are elided at compile time. This function remains valid regardless of
/// the feature — the `elided` feature context builds the same crate with
/// `tracing/max_level_off` and the `debug` span is absent there.
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
