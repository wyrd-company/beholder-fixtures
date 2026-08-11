//! Edition 2018 crate demonstrating uniform paths (no `extern crate` required).

use fixture_direct::DirectType;

// Edition 2018+: `fixture_direct::DirectType` resolves via extern prelude without `extern crate`.
// Leading `::fixture_direct` is still accepted but considered legacy; `crate::` is preferred.
pub fn edition2018_uniform_path() -> DirectType {
    DirectType::new(18)
}

pub fn edition2018_leading_colons_still_works() -> ::fixture_direct::DirectType {
    ::fixture_direct::DirectType::new(180)
}

pub fn edition2018_macro_via_use() -> u32 {
    // In 2018+, macros are imported via `use`.
    use fixture_direct::direct_macro;
    direct_macro!()
}
