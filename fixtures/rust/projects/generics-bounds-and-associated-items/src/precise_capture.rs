// RS-CAN-GEN-008: opaque-type precise capture contrasting edition 2021 and 2024
// with explicit use<...> control. This crate is edition 2024: RPIT captures
// every in-scope generic by default (not only generics used by the hidden type).

// Captures lifetime precisely via explicit use<'a>; opaque holds the borrow.
pub fn captures_lifetime<'a>(value: &'a u32) -> impl Clone + use<'a> {
    value
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
    (value, N)
}

// Edition 2024 default: without explicit use<...>, RPIT captures every
// in-scope generic. This function without explicit use captures 'a by default
// in edition 2024, equivalent to `impl Clone + use<'a>`.
#[allow(clippy::needless_lifetimes)]
pub fn default_capture_2024<'a>(value: &'a u32) -> impl Clone {
    value
}

// Unused-generic default: even though hidden type does not use 'a,
// edition 2024 still captures every in-scope generic, so borrow is held.
#[allow(clippy::needless_lifetimes)]
pub fn default_unused_2024<'a>(value: &'a u32) -> impl Clone {
    let _ = value;
    42u32
}

// Explicit empty capture in edition 2024: overrides the default and captures nothing.
pub fn default_capture_overridden_empty<'a>(value: &'a u32) -> impl Clone + use<> {
    let _ = value;
    42u32
}

// Borrow-acceptance contrast: capturing opaque prevents mutation while live,
// empty capture allows mutation. Both are valid and demonstrate the semantic difference.
pub fn demo_capturing_prevents_mutation() {
    let mut value = 0u32;
    {
        let guard = captures_lifetime(&value);
        // value = 1; // would be rejected: cannot mutate while `guard` holds borrow
        let _ = &guard;
    }
    value = 1; // allowed after guard dropped
}

pub fn demo_empty_allows_mutation() {
    let mut value = 0u32;
    let guard = empty_capture();
    value = 1; // allowed: guard captures nothing
    let _ = guard;
}

pub fn demo_default_captures() {
    let mut value = 0u32;
    {
        let guard = default_capture_2024(&value);
        // value = 1; // would be rejected in edition 2024 because default captures 'a
        let _ = &guard;
    }
    value = 1;
}

pub fn demo_explicit_empty_overrides() {
    let mut value = 0u32;
    let guard = default_capture_overridden_empty(&value);
    value = 1; // allowed: explicit use<> overrides default capture
    let _ = guard;
}

pub fn demo_default_unused_captures() {
    let mut value = 0u32;
    {
        let guard = default_unused_2024(&value);
        // value = 1; // would be rejected in edition 2024: default captures 'a even though unused
        let _ = &guard;
    }
    value = 1;
}

// Nested opaque type via helper function.
fn nested_helper<'a>(value: &'a str) -> impl Clone + use<'a> {
    value
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
    value
}

// Trait method RPIT restriction: traits cannot declare precise capture with
// use<...> in the same way as inherent functions (documented). We provide a
// valid inherent method RPIT as contrast.
pub struct Capturer;

impl Capturer {
    pub fn capture_self<'a>(&'a self, value: &'a str) -> impl Clone + use<'a> {
        value
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
    value
}

pub fn precise_capture_summary() -> &'static str {
    "precise_capture_2024"
}
