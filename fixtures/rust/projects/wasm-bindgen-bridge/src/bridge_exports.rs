//! Exported Rust-to-foreign surface via `#[wasm_bindgen]`.
//!
//! Each item below is exported through the wasm-bindgen bridge, not through
//! ordinary `pub` or `extern "C"`. The macro expands on the host into glue
//! that exposes a JS-callable surface when built for `wasm32-unknown-unknown`.

use wasm_bindgen::prelude::*;

/// Simple numeric export — crosses the ABI as a Wasm `i32` pair.
///
/// Visible to JavaScript as `add(a, b)` with number-to-i32 coercion supplied
/// by the generated glue, distinct from `plain_exports::c_exported_add`.
#[wasm_bindgen]
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

/// String-returning export — demonstrates ABI adaptation for UTF-8 strings.
///
/// Rust `&str`/`String` are not passed as raw pointers; the generated glue
/// allocates linear-memory bytes, encodes UTF-8, and arranges deallocation.
#[wasm_bindgen]
pub fn greet(name: &str) -> String {
    format!("Hello, {name}!")
}

/// Owning-string concatenation — ownership transfer from JS to Rust and back.
#[wasm_bindgen]
pub fn concat_strings(a: String, b: String) -> String {
    format!("{a}{b}")
}

/// Ownership via `Vec<u8>` — JS `Uint8Array` ↔ Rust `Vec<u8>` adaptation.
#[wasm_bindgen]
pub fn create_buffer(size: usize) -> Vec<u8> {
    vec![0u8; size]
}

/// Optional string handling — `Option<String>` maps to `string | undefined` in JS.
#[wasm_bindgen]
pub fn optional_greeting(name: Option<String>) -> String {
    match name {
        Some(n) => format!("Hello, {n}!"),
        None => "Hello!".to_string(),
    }
}

/// Boolean and float exports — primitive ABI mapping to JS booleans/numbers.
#[wasm_bindgen]
pub fn is_even(n: i32) -> bool {
    n % 2 == 0
}

#[wasm_bindgen]
pub fn scale(value: f64, factor: f64) -> f64 {
    value * factor
}

/// Exported struct — exposed as a JS class with constructor and methods.
///
/// Field access is not `pub` in the Rust sense; accessors are generated via
/// `#[wasm_bindgen]` getter/setter and method glue.
#[wasm_bindgen]
pub struct BridgeCounter {
    value: i32,
}

#[wasm_bindgen]
impl BridgeCounter {
    #[wasm_bindgen(constructor)]
    pub fn new(initial: i32) -> BridgeCounter {
        BridgeCounter { value: initial }
    }

    pub fn increment(&mut self) {
        self.value += 1;
    }

    pub fn value(&self) -> i32 {
        self.value
    }

    #[wasm_bindgen(getter)]
    pub fn count(&self) -> i32 {
        self.value
    }

    #[wasm_bindgen(setter)]
    pub fn set_count(&mut self, value: i32) {
        self.value = value;
    }

    pub fn add_to(&mut self, delta: i32) -> i32 {
        self.value += delta;
        self.value
    }
}

/// Exported enum — mapped to a JS numeric object by the bridge.
///
/// Distinct from a C `#[repr(u32)]` enum exported via `extern "C"`.
#[wasm_bindgen]
pub enum BridgeStatus {
    Idle = 0,
    Active = 1,
    Done = 2,
}

#[wasm_bindgen]
pub fn status_label(status: BridgeStatus) -> String {
    match status {
        BridgeStatus::Idle => "idle".to_string(),
        BridgeStatus::Active => "active".to_string(),
        BridgeStatus::Done => "done".to_string(),
    }
}
