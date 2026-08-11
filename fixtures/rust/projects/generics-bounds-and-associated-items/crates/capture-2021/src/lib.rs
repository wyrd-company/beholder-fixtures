// RS-CAN-GEN-008: edition 2021 contrast for opaque precise capture.
// In edition 2021 the default capture for RPIT is the pre-2024 capture rules.
// Explicit use<...> (stable 1.82) still controls the set, but the default differs.

// In 2021, `fn legacy_default<'a>(value: &'a u32) -> impl Clone { *value }`
// would capture under the 2021 rules, which do not precisely track lifetimes
// the same way 2024 does. The explicit forms below compile identically, but
// document the edition-contrast.

// Captures lifetime with explicit set (same syntax in both editions).
pub fn captures_lifetime<'a>(value: &'a u32) -> impl Clone + use<'a> {
    *value
}

// Empty capture set (no generics).
pub fn empty_capture() -> impl Clone + use<> {
    42u32
}

// Captures type parameter.
pub fn captures_type<T: Clone>(value: T) -> impl Clone + use<T> {
    value
}

// Captures const parameter.
pub fn captures_const<const N: usize>() -> impl Clone + use<N> {
    N
}

// Legacy default without explicit use: in 2021 this follows 2021 capture rules.
// In 2024 the same signature would be `use<'a>` implicitly.
#[allow(clippy::needless_lifetimes)]
pub fn legacy_default_capture<'a>(value: &'a u32) -> impl Clone {
    *value
}

// Demonstrates explicit non-empty set matching the 2024 default capture.
pub fn explicit_matching_default<'a>(value: &'a u32) -> impl Clone + use<'a> {
    *value
}

// Multiple capture set in 2021 syntax.
pub fn captures_all<'a, T: Clone, const N: usize>(value: &'a T) -> impl Clone + use<'a, T, N>
where
    T: 'a,
{
    (value.clone(), N)
}

pub fn summary() -> &'static str {
    "precise_capture_2021"
}
