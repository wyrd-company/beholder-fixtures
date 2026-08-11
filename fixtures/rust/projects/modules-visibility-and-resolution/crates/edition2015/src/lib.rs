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
