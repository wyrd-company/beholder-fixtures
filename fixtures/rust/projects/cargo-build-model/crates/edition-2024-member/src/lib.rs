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

// RS-CAN-PROJ-016: edition-2024-sensitive construct — since edition 2024,
// `extern` blocks must be written as `unsafe extern` (RFC 3484). Compiling
// this block without `unsafe` under an earlier edition is a hard error
// ("extern blocks must be unsafe"); see `coverage.md` for the counterexample.
unsafe extern "C" {
    fn abs(x: i32) -> i32;
}

#[allow(clippy::all)]
pub fn edition_2024_specific() -> i32 {
    unsafe { abs(-7) }
}
