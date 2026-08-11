//! RS-CAN-PROJ-016: edition 2018.

#[macro_export]
macro_rules! cross_edition_macro_2018 {
    () => {
        2018
    };
}

pub fn edition_id() -> &'static str {
    "2018"
}

// RS-CAN-PROJ-016: edition-2018 "uniform paths" — a `use` import of an external
// crate resolves directly by crate name since edition 2018, without an
// `extern crate` declaration. Edition 2015 requires `extern crate edition_2015;`
// first, or this `use` fails to resolve (`error[E0432]: unresolved import`; see
// `crates/edition-2015` and `coverage.md` for the counterexample).
use edition_2015::edition_id as edition_2015_id;

pub fn uniform_path_demo() -> &'static str {
    edition_2015_id()
}
