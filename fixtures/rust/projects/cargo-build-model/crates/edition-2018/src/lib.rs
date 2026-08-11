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

// 2018 edition: `async` and `await` are keywords, `try` not.
// Leading `::` edition-2015 vs 2018+ difference documented in coverage.
// 2018 removed `extern crate` requirement for std.
pub fn edition_2018_feature() -> u32 {
    let v = vec![1, 2, 3];
    v.into_iter().sum()
}
