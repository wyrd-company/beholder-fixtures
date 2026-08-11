//! RS-CAN-PROJ-016: edition 2024 with mixed-edition graph.
//! Interacting crates on 2015, 2018, 2021, and 2024 with edition-sensitive constructs.
//! Macro defined in 2015 crate invoked from 2024 crate (cross-edition macro).

use edition_2015::cross_edition_macro;

pub fn edition_id() -> &'static str {
    "2024"
}

// Cross-edition macro: defined in 2015, invoked from 2024
pub fn cross_macro_user() -> u32 {
    cross_edition_macro!()
}

// Use all editions to prove interoperability in one graph.
pub fn all_editions() -> Vec<&'static str> {
    vec![
        edition_2015::edition_id(),
        edition_2018::edition_id(),
        edition_2021::edition_id(),
        edition_id(),
    ]
}

// 2024 edition sensitive: let chains (1.88+ with 2024), unsafe syntax changes.
#[allow(clippy::all)]
pub fn edition_2024_specific() -> u32 {
    let x = Some(5);
    if let Some(v) = x { v } else { 0 }
}
