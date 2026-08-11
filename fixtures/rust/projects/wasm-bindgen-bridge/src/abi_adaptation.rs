//! ABI adaptation detail for the bridge.
//!
//! Primitive and composite Rust types are lowered to Wasm ABI types (`i32`,
//! `i64`, `f32`, `f64`) plus linear-memory string/bytes handling. The glue
//! converts JS `number`/`boolean`/`string` values to those ABI positions and
//! back. This is distinct from `extern "C"` where callers deal in raw pointers.

use wasm_bindgen::prelude::*;

/// Primitive ABI — numbers and booleans cross by value.
///
/// JS `number` ↔ `i32`/`f64` and JS `boolean` ↔ `bool` are mapped without pointer
/// intermediates. The bridge inserts narrow/widen and JS-type coercion as needed.
#[wasm_bindgen]
pub fn primitive_add(a: i32, b: i32) -> i32 {
    a + b
}

#[wasm_bindgen]
pub fn primitive_scale(value: f64, factor: f64) -> f64 {
    value * factor
}

#[wasm_bindgen]
pub fn primitive_negate(flag: bool) -> bool {
    !flag
}

/// String ABI — UTF-8 bytes in linear memory with length.
///
/// The glue calls `__wbindgen_malloc`/`__wbindgen_free` to place/retire the
/// byte buffer; the callee never receives a bare `*const u8`.
#[wasm_bindgen]
pub fn string_abi_len(s: &str) -> usize {
    s.len()
}

#[wasm_bindgen]
pub fn string_abi_concat(a: String, b: String) -> String {
    format!("{a}{b}")
}

/// Bytes ABI — `Vec<u8>` is `Uint8Array` on the JS side.
///
/// Length and pointer are passed through wasm-bindgen's vector adapter rather
/// than a hand-written C-ABI `*const u8, usize` pair.
#[wasm_bindgen]
pub fn bytes_abi_sum(data: Vec<u8>) -> usize {
    data.len()
}

/// Optional ABI — `Option<T>` introduces a presence discriminant.
///
/// The glue represents `None` as `undefined` (or `null`) and `Some(v)` as the
/// value, with a separate stack slot for the discriminant when lowered.
#[wasm_bindgen]
pub fn optional_abi(value: Option<String>) -> bool {
    value.is_some()
}

/// Result ABI — `Result<T, JsValue>` maps Rust error to JS exception.
///
/// `Ok(v)` returns the value; `Err(e)` throws `e` via `wasm_bindgen::JsValue`.
#[wasm_bindgen]
pub fn result_abi(value: i32) -> Result<i32, JsValue> {
    if value >= 0 {
        Ok(value)
    } else {
        Err(JsValue::from_str("negative"))
    }
}

/// Struct ABI — a `#[wasm_bindgen]` struct crosses as an opaque JS handle.
///
/// Construction returns a boxed Rust value revealed as a JS class instance;
/// method calls dispatch through the generated wrapper table.
#[wasm_bindgen]
pub struct AbiHolder {
    inner: i32,
}

#[wasm_bindgen]
impl AbiHolder {
    #[wasm_bindgen(constructor)]
    pub fn new(inner: i32) -> AbiHolder {
        AbiHolder { inner }
    }

    pub fn get(&self) -> i32 {
        self.inner
    }

    pub fn set(&mut self, value: i32) {
        self.inner = value;
    }
}

/// Marker for coverage.
pub fn abi_label() -> &'static str {
    let _ = primitive_add(1, 2);
    let _ = primitive_scale(1.0, 2.0);
    let _ = primitive_negate(true);
    let _ = string_abi_len("x");
    let _ = string_abi_concat("a".to_string(), "b".to_string());
    let _ = bytes_abi_sum(vec![1]);
    let _ = optional_abi(Some("x".to_string()));
    let _ = result_abi(1);
    let mut h = AbiHolder::new(1);
    let _ = h.get();
    h.set(2);
    "abi-adaptation"
}
