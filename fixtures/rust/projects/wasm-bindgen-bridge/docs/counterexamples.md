# Counterexamples (documentation only — never compiled)

Invalid or non-installed bridge configurations are documented here. None are
compiled as Rust source in this fixture. Each preserves the contrast noted in
the assignment brief while the valid `wasm32-unknown-unknown` + `wasm-bindgen`
bridge is the only implementation.

## RS-CAN-ECO-008 — Cross-language and Wasm bridge generators

### Non-installed alternative Wasm ABI or interface generator

```rust,ignore
// WASI bridge (`wasm32-wasip1`) is not the target exercised here.
// A WASI-targeted bridge would require `wasm32-wasip1` in rustup and a WASI
// runtime import set, rather than the `wasm32-unknown-unknown` + browser/JS
// imports used here. This project builds only for `wasm32-unknown-unknown`.
//
// A C++ bridge (e.g., `cxx`/`autocxx`) or a Python bridge (e.g., `pyo3`) would
// similarly need its own foreign companion and target installation. None are
// present; only `wasm-bindgen` is pinned and vendored for the wasm bridge.
// The alternative generators are therefore documented here and not compiled.
```

```rust,ignore
// Alternate IDL/interface generator (e.g., `wit-bindgen` via WIT) is a
// component-model generator rather than the `wasm-bindgen` macro bridge.
// Its attributes, generated glue directory layout, and JS companion artifact
// names differ from `wasm-bindgen`. No `wit-bindgen` dependency or generated
// WIT-derived source is tracked in this crate.
```

### Companion foreign artifact produced only by downstream tool

```rust,ignore
// `wasm-bindgen-cli` produces `*_bg.js` / `*_bg.wasm` glue when run against a
// built `cdylib` artifact. That JS glue file contains the allocation adapters
// (`__wbindgen_malloc`, `__wbindgen_free`, UTF-8 encode/decode) and import
// wiring for `console.log`/`alert`. This fixture purposely does not execute
// `wasm-bindgen` or `wasm-pack`; the `build` task remains `cargo build`
// offline. The JS glue existence and naming are documented-level detail, not a
// Rust identifier checked into the tree.
```

```rust,ignore
// `wasm-pack test` / `wasm-opt` post-processing would produce further foreign
// artifacts (bundler/packager output, optimized Wasm). Those are companion
// products of downstream tools, not Rust source entities, and are not tracked.
```

### Generated foreign-binding details are documentation-level

```rust,ignore
// The precise JS symbol emitted for `BridgeCounter::increment` (e.g.,
// `bridge_counter_increment`) and the linear-memory `passStringToWasm0` helper
// name are generated glue internals determined by the `wasm-bindgen` macro
// version. They are visible in the compiled Wasm custom section and in the JS
// glue, but they are not Rust-visible identifiers and are not asserted as
// `cargo test` names. Coverage locators refer to the `#[wasm_bindgen]` Rust
// declarations that cause the glue, not to the generated JS identifiers.
```

### Tool version / host generator contrast

```rust,ignore
// `wasm-bindgen = "=0.2.100"` is the pinned host generator. The macro runs on
// the host (proc-macro) during `cargo build`, not on the wasm target. Upgrading
// to a later `wasm-bindgen` without also syncing `wasm-bindgen-cli` would make
// the custom section version disagree with the CLI decoder — this version skew
// is the tool-version failure preserved here as documentation.
```

### Target contrast that is not exercised

```rust,ignore
// Building for `wasm32-wasip1` (WASI `unknown`'s WASI sibling) would require
// the `wasm32-wasip1` target and a WASI reactor/import set. Only
// `wasm32-unknown-unknown` is installed and exercised by `Taskfile build`.
```
