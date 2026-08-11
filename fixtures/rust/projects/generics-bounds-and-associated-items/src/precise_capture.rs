// RS-CAN-GEN-008: opaque-type precise capture contrasting edition 2021 and 2024
// with explicit use<...> control. This module is edition 2024: default capture
// for RPIT is precise (captures in-scope generics used by the hidden type).

// Captures lifetime precisely via explicit use<'a>.
pub fn captures_lifetime<'a>(value: &'a u32) -> impl Clone + use<'a> {
    *value
}

// Empty capture set: hidden type captures nothing (no generics in scope).
pub fn empty_capture() -> impl Clone + use<> {
    42u32
}

// Nonempty capture set capturing type parameter.
pub fn captures_type<T: Clone>(value: T) -> impl Clone + use<T> {
    value
}

// Captures const parameter.
pub fn captures_const<const N: usize>() -> impl Clone + use<N> {
    N
}

// Captures multiple: lifetime, type, and const together.
pub fn captures_all<'a, T: Clone, const N: usize>(value: &'a T) -> impl Clone + use<'a, T, N>
where
    T: 'a,
{
    (value.clone(), N)
}

// Edition 2024 default precise capture: without explicit use<...>, the compiler
// captures exactly the generics used. This function demonstrates the 2024 default
// where 'a is captured because it is used in the hidden type.
#[allow(clippy::needless_lifetimes)]
pub fn default_capture_2024<'a>(value: &'a u32) -> impl Clone {
    // In edition 2024, this is equivalent to impl Clone + use<'a>.
    *value
}

// Nested opaque type via helper function.
fn nested_helper<'a>(value: &'a str) -> impl Clone + use<'a> {
    value.to_owned()
}

pub fn nested_opaque<'a>(value: &'a str) -> impl Clone + use<'a> {
    nested_helper(value)
}

// Argument-position impl Trait (APTI) is distinct from RPIT; here we show
// RPIT with precise capture contrasted to APTI which cannot use precise capture
// in the same way (documented in counterexamples).
pub fn takes_impl_trait(value: u32) -> impl Clone + use<> {
    let _ = value;
    0u8
}

// Generic function whose RPIT captures inferred lifetime via precise capture.
pub fn inferred_capture(value: &str) -> impl Clone + use<'_> {
    value.to_owned()
}

// Trait method RPIT restriction: traits cannot declare precise capture with
// use<...> in the same way as inherent functions (documented). We provide a
// valid inherent method RPIT as contrast.
pub struct Capturer;

impl Capturer {
    pub fn capture_self<'a>(&'a self, value: &'a str) -> impl Clone + use<'a> {
        value.to_owned()
    }

    pub fn no_capture(&self) -> impl Clone + use<> {
        1u32
    }
}

// Explicit capture of lifetime and type together, showing nonempty set.
pub fn explicit_nonempty<'a, T>(value: &'a T) -> impl Clone + use<'a, T>
where
    T: Clone + 'a,
{
    value.clone()
}

pub fn precise_capture_summary() -> &'static str {
    "precise_capture_2024"
}
