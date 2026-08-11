//! RS-CAN-PROJ-016: edition 2021.

#[macro_export]
macro_rules! cross_edition_macro_2021 {
    () => {
        2021
    };
}

pub fn edition_id() -> &'static str {
    "2021"
}

// 2021 edition: arrays `IntoIterator` changed, closure capture rules.
pub fn into_iter_demo() -> u32 {
    let arr = [1, 2, 3];
    arr.into_iter().sum()
}

// 2021 prelude addition: `panic!` with new handling, etc.
pub fn closure_capture_demo() -> u32 {
    let x = 5;
    let c = || x + 1;
    c()
}
