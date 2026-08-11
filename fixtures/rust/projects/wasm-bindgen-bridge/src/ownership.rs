//! Ownership and ABI adaptation across the bridge.
//!
//! `wasm-bindgen` inserts allocation/copy glue so Rust and JS ownership
//! discipline each remain valid while crossing the boundary. Strings and bytes
//! are copied between linear memory and JS GC memory; numeric types map by value.

use wasm_bindgen::prelude::*;

/// Borrowed string — JS `string` is borrowed as `&str` without taking ownership.
///
/// The caller (JS) retains ownership; Rust sees a borrowed view produced by the
/// glue's temporary UTF-8 decoding. No `String` allocation is returned to JS.
#[wasm_bindgen]
pub fn borrowed_len(s: &str) -> usize {
    s.len()
}

/// Owned string — JS transfers ownership to Rust as `String`.
///
/// The glue copies the JS string bytes into Wasm memory and Rust takes ownership
/// of the resulting `String`; the JS GC value remains collectable.
#[wasm_bindgen]
pub fn owned_echo(s: String) -> String {
    s
}

/// Mutable slice adaptation via `Vec<u8>` — ownership transfer for bytes.
///
/// `Vec<u8>` and `Uint8Array` are the idiomatic bridge for bytes. The glue
/// copies bytes across the boundary; Rust owns the `Vec` after the call.
#[wasm_bindgen]
pub fn bytes_sum(bytes: Vec<u8>) -> u32 {
    bytes.iter().map(|&b| b as u32).sum()
}

/// Producing owned bytes — Rust allocates, JS receives a new `Uint8Array`.
#[wasm_bindgen]
pub fn owned_bytes(size: usize) -> Vec<u8> {
    vec![0xAB; size]
}

/// Optional ownership — `Option<String>` maps to `string | undefined`.
///
/// `None` becomes `undefined` on the JS side; `Some` becomes a JS string value.
#[wasm_bindgen]
pub fn echo_optional(s: Option<String>) -> Option<String> {
    s
}

/// Returning a struct demonstrates ownership of a JS-class instance.
///
/// `BridgeValue` is constructed on Rust's side and moved into JS GC ownership
/// via the generated wrapper.
#[wasm_bindgen]
pub struct BridgeValue {
    payload: String,
}

#[wasm_bindgen]
impl BridgeValue {
    #[wasm_bindgen(constructor)]
    pub fn new(payload: String) -> BridgeValue {
        BridgeValue { payload }
    }

    #[wasm_bindgen(getter)]
    pub fn payload(&self) -> String {
        self.payload.clone()
    }

    pub fn into_payload(self) -> String {
        self.payload
    }
}

/// Composite ownership demo keeping the symbols referenced.
pub fn ownership_label() -> &'static str {
    // Keep symbols observed for graph extraction.
    let _ = borrowed_len("x");
    let _ = owned_echo("y".to_string());
    let _ = bytes_sum(vec![1, 2]);
    let _ = owned_bytes(2);
    let _ = echo_optional(Some("z".to_string()));
    let v = BridgeValue::new("payload".to_string());
    let _ = v.payload();
    "ownership-abi"
}
