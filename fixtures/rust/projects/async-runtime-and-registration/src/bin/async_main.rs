//! Binary entry point demonstrating `#[tokio::main]` rewriting — RS-CAN-ECO-003.
//!
//! Source: `#[tokio::main] async fn main()` (stacked with `#[tracing::instrument]`
//! on the same item to demonstrate macro stacking).
//! Compiled (pinned Tokio 1.47.1): synchronous `fn main()` containing a local
//! `async move` body passed to `Builder::new_multi_thread().enable_all().build().unwrap().block_on`,
//! with no hidden module; the tracing wrapper creates an `INFO` span around
//! the body.

#[tracing::instrument]
#[tokio::main(flavor = "current_thread")]
async fn main() {
    // Body wrapped by the attribute; runs inside the Tokio runtime.
    let value = async_runtime_and_registration::instrumentation::async_instrumented_work(7).await;
    assert_eq!(value, 8);

    let doubled = async_runtime_and_registration::instrumentation::instrumented_add(2, 3);
    assert_eq!(doubled, 5);

    // Exercise registration from the binary as well.
    let plugins = async_runtime_and_registration::registration::all_plugin_names();
    assert!(plugins.contains(&"alpha"));
    assert!(plugins.contains(&"beta"));

    println!("async-runtime-and-registration: main ok, plugins={plugins:?}");
}
