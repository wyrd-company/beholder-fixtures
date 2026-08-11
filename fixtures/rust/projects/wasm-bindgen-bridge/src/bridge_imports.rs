//! Imported foreign items via `#[wasm_bindgen] extern "C"`.
//!
//! These are JS-provided symbols imported into Wasm. They do not exist as
//! Rust `pub` items and are not `extern "C"` link symbols in the native sense;
//! the wasm-bindgen glue turns them into `wasm import` entries whose names and
//! namespaces come from the `#[wasm_bindgen]` attributes.

use wasm_bindgen::prelude::*;

/// Foreign imports from JavaScript.
///
/// `alert` and `console.log` are provided by the JS environment. The bridge
/// macro records module/name metadata and generates an import in the Wasm module
/// that the JS glue satisfies. The imported functions handle string UTF-8
/// decoding on entry and do not use C-ABI `*const c_char`.
#[wasm_bindgen]
extern "C" {
    fn alert(s: &str);

    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);

    #[wasm_bindgen(js_namespace = console, js_name = log)]
    fn console_log_number(n: f64);

    #[wasm_bindgen(js_name = Math_random)]
    fn math_random() -> f64;
}

/// `js_namespace` + `js_name` combination for a namespaced foreign call.
pub fn imported_console_log(message: &str) {
    log(message);
}

/// Calling an imported that borrows a string — ownership stays with Rust.
pub fn imported_alert(message: &str) {
    alert(message);
}

/// Calling an imported that returns a primitive via ABI adaptation.
pub fn imported_random_scaled(factor: f64) -> f64 {
    math_random() * factor
}

/// Calling a console logger for a number value.
pub fn imported_log_number(n: f64) {
    console_log_number(n);
}

/// Marker describing the imported surface for coverage.
pub fn imported_surface_label() -> &'static str {
    "imports"
}

/// Wasm-gated host fallback used when not targeting wasm.
///
/// On `wasm32` the calls above resolve via Wasm imports. Off-target they would
/// trap without a JS engine; the target-gated wrapper in `wasm_target` provides
/// a host fallback, while this module retains the pure import shape.
pub fn host_fallback_demo(message: &str) -> String {
    if cfg!(target_arch = "wasm32") {
        imported_alert(message);
        format!("wasm-import:{message}")
    } else {
        format!("host-fallback:{message}")
    }
}
