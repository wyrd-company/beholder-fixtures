// RS-CAN-GEN-008: edition 2021 contrast for opaque precise capture.
// In edition 2021 the default capture for RPIT is the pre-2024 rule: it does not
// capture every in-scope generic by default. Explicit use<...> (stable 1.82)
// controls the set, but the default differs from edition 2024.

// In 2021, `fn legacy_default<'a>(value: &'a u32) -> impl Clone { value }`
// returns an opaque that does not capture 'a by default, unlike edition 2024
// where the same signature would be equivalent to `impl Clone + use<'a>`.

// Captures lifetime with explicit set (same syntax in both editions).
pub fn captures_lifetime<'a>(value: &'a u32) -> impl Clone + use<'a> {
    value
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

// Legacy default without explicit use: in 2021 this follows pre-2024 capture
// rules and does not capture 'a by default.
#[allow(clippy::needless_lifetimes)]
pub fn legacy_default_capture<'a>(value: &'a u32) -> impl Clone {
    *value
}

// Demonstrates explicit nonempty set matching the edition 2024 default capture.
pub fn explicit_matching_default<'a>(value: &'a u32) -> impl Clone + use<'a> {
    value
}

// Multiple capture set in 2021 syntax.
pub fn captures_all<'a, T: Clone, const N: usize>(value: &'a T) -> impl Clone + use<'a, T, N>
where
    T: 'a,
{
    (value, N)
}

// Unused-generic in 2021: default does not capture 'a when hidden type does not use it.
#[allow(clippy::needless_lifetimes)]
pub fn legacy_default_unused<'a>(value: &'a u32) -> impl Clone {
    let _ = value;
    42u32
}

// Explicit capture of unused generic in 2021 still holds borrow.
pub fn explicit_unused_capture<'a>(value: &'a u32) -> impl Clone + use<'a> {
    let _ = value;
    42u32
}

// Edition 2021 borrow-acceptance contrast: legacy default allows mutation while
// opaque is live, explicit capture prevents it. In edition 2024 the default
// would prevent mutation like the explicit form.
pub fn demo_legacy_allows_mutation() {
    let mut value = 0u32;
    let guard = legacy_default_capture(&value);
    value = 1; // allowed in 2021: default does not capture 'a
    let _ = guard;
}

pub fn demo_explicit_prevents_mutation() {
    let mut value = 0u32;
    {
        let guard = explicit_matching_default(&value);
        // value = 1; // would be rejected: explicit use<'a> captures borrow
        let _ = &guard;
    }
    value = 1;
}

pub fn demo_legacy_unused_allows_mutation() {
    let mut value = 0u32;
    let guard = legacy_default_unused(&value);
    value = 1; // allowed in 2021: default does not capture unused 'a
    let _ = guard;
}

pub fn demo_explicit_unused_prevents() {
    let mut value = 0u32;
    {
        let guard = explicit_unused_capture(&value);
        // value = 1; // would be rejected: explicit use<'a> captures even unused
        let _ = &guard;
    }
    value = 1;
}

pub fn summary() -> &'static str {
    "precise_capture_2021"
}
