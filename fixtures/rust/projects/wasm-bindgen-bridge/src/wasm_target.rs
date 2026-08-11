//! Target gating, link behavior, and companion-artifact notes.
//!
//! The bridge surface is always *present* for type-checking on the host, but
//! its Wasm glue (generated wasm custom sections, `__wbindgen_*` symbols, and
//! JS glue import/export records) is only linked when the crate is built for
//! `wasm32-unknown-unknown`. The downstream `wasm-bindgen` CLI companion that
//! emits `*.js`/`*_bg.wasm` is intentionally not executed here.

use wasm_bindgen::prelude::*;

/// Target-gated entry — illustrates `cfg(target_arch = "wasm32")` gating.
///
/// The wasm-bindgen attribute is applied in both variants; the inner body is
/// gated so host builds exercise ordinary control flow while wasm builds
/// exercise the imported JS glue path.
#[cfg(target_arch = "wasm32")]
#[wasm_bindgen]
pub fn wasm_only_entry(value: u32) -> u32 {
    // On wasm, this bodies a plausible glue-assisted branch.
    value.wrapping_mul(2)
}

#[cfg(not(target_arch = "wasm32"))]
#[wasm_bindgen]
pub fn wasm_only_entry(value: u32) -> u32 {
    value.wrapping_mul(2)
}

/// Target-gated linker marker — shows that the wasm section `__wasm_bindgen_*`
/// is emitted only for the wasm target.
///
/// Host builds keep the item valid but without the Wasm link contract.
#[cfg(target_arch = "wasm32")]
#[wasm_bindgen]
pub fn wasm_section_marker() -> u32 {
    0xDEAD
}

#[cfg(not(target_arch = "wasm32"))]
pub fn wasm_section_marker() -> u32 {
    0xDEAD
}

/// Branded helper illustrating comparison with the non-wasm artifact set.
///
/// Building for `wasm32-unknown-unknown` produces wasm imports/exports and a
/// custom section that host `x86_64-unknown-linux-gnu` builds only type-check.
/// The JS companion (`*_bg.js`) generation via `wasm-bindgen-cli` is a
/// downstream tool step not executed by `Taskfile build`.
pub fn wasm_target_label() -> &'static str {
    if cfg!(target_arch = "wasm32") {
        "wasm32-unknown-unknown"
    } else {
        "host"
    }
}

/// Demonstrates calling an imported item with a host fallback.
///
/// Validates that the import in `bridge_imports` is linked on wasm but has a
/// coherent host behavior (no trap) when compiled natively.
pub fn call_import_with_fallback(message: &str) -> String {
    crate::bridge_imports::host_fallback_demo(message)
}
