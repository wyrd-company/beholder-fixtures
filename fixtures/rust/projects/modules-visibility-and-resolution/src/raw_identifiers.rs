// RS-CAN-MOD-013: raw identifiers for keyword spellings and non-ASCII identifier.

// Older-edition keyword `try` exported from 2015 crate via raw identifier, consumed here in 2024.
// Demonstrates cross-edition raw identifier export.
use fixture_edition2015::r#try as old_edition_try;
use fixture_edition2015::r#type as OldEditionType;

// Local 2024 raw identifiers for keyword spellings.
pub fn r#try() -> u32 {
    999
}

#[allow(non_camel_case_types)]
pub struct r#type {
    pub value: u32,
}

impl r#type {
    pub fn new(v: u32) -> Self {
        Self { value: v }
    }
}

pub struct WithKeywordField {
    pub r#match: u32,
    pub r#async: u32,
}

// Non-ASCII identifier with composed form.
pub fn naïve_café() -> u32 {
    42
}

pub struct Café {
    pub déjà_vu: u32,
}

impl Café {
    pub fn naïve_method(&self) -> u32 {
        self.déjà_vu
    }
}

// Unicode identifier with Greek capital Delta (non-ASCII, distinct from ASCII `delta`).
pub fn unicode_identifier_demo() -> u32 {
    let café = 10u32;
    let naïve = café + 5;
    let Δ = naïve + 2; // Greek Delta U+0394
    Δ
}

// Normalization-equivalent spelling: `café` composed (U+00E9) normalizes same as decomposed `e` + U+0301.
// Rust normalizes identifiers via NFKC, so `café` (composed) and `cafe\u{0301}` (decomposed) are same identifier – defining both would be duplicate.
// Valid single form:
pub fn café_composed() -> u32 {
    77
}

// Confusable identifiers – visually similar but distinct codepoints.
// `item` (Latin) vs `itеm` (Cyrillic е U+0435) – same visual, different identifier.
pub fn confusable_demo() -> u32 {
    let item = 1;
    let itеm = 2; // second `е` is Cyrillic U+0435, confusable with Latin `e`
    item + itеm
}

// Uncommon codepoint: Greek alpha `α` (U+03B1) is valid but uncommon in Rust identifiers.
pub fn uncommon_codepoint_demo() -> u32 {
    let α = 10u32;
    let β = 20u32;
    α + β
}

// Cross-edition consumption of older-edition keyword-named item.
pub fn call_raw_identifiers() -> u32 {
    let t = r#type::new(5);
    let s = WithKeywordField {
        r#match: 1,
        r#async: 2,
    };
    let old = old_edition_try();
    let old_type = OldEditionType { v: 6 };
    let _ = old_type;
    t.value
        + s.r#match
        + s.r#async
        + r#try()
        + naïve_café()
        + unicode_identifier_demo()
        + old
        + café_composed()
        + confusable_demo()
        + uncommon_codepoint_demo()
}

pub fn r#gen() -> u32 {
    777
}

// Demonstrate raw identifier for keyword as field and method via older edition.
pub fn cross_edition_raw_field() -> u32 {
    let x = fixture_edition2015::CrossEditionRaw { r#match: 3 };
    x.r#match + fixture_edition2015::r#try()
}
