//! Edition 2015 crate demonstrating legacy `extern crate` and `macro_use` semantics.

#[macro_use]
extern crate fixture_direct;

// In edition 2015, `::fixture_direct::DirectType` via leading `::` is the old absolute path grammar.
// Modern edition 2024 treats `crate::` as primary; leading `::` remains legacy.
pub fn edition2015_leading_colons() -> ::fixture_direct::DirectType {
    ::fixture_direct::DirectType::new(15)
}

// Legacy macro import via `#[macro_use] extern crate` makes macro available without import.
pub fn edition2015_macro_use() -> u32 {
    direct_macro!()
}

pub fn cross_edition_type() -> fixture_direct::DirectType {
    fixture_direct::DirectType::new(150)
}

// Cross-edition raw identifier: in 2015, `try` was not yet a strict keyword, but `r#try` is still valid raw spelling.
// This item is exported to 2024 consumer via raw identifier `r#try`.
#[allow(non_camel_case_types)]
pub fn r#try() -> u32 {
    1500
}

pub struct r#type {
    pub v: u32,
}

// Keyword-named field via raw identifier, also cross-edition.
pub struct CrossEditionRaw {
    pub r#match: u32,
}

// Edition 2021 prelude addition: `TryInto` in prelude since 2021, but in 2015 must be explicitly imported.
// Valid in 2015 with explicit `use`.
pub fn edition2015_try_into(x: u8) -> u16 {
    use std::convert::TryInto;
    x.try_into().unwrap()
}
