#![allow(dead_code)]

// RS-CAN-MAC-001: edition 2021 fragment grammar pat vs pat_param
// `pat` allows top-level or-pattern `A | B`, `pat_param` is used where leading `|` is not part of the param
#[macro_export]
macro_rules! pat_2021_demo {
    ($p:pat) => {
        match 10u32 {
            $p => 1u32,
            _ => 0u32,
        }
    };
}

#[macro_export]
macro_rules! pat_param_2021_demo {
    ($p:pat_param) => {{
        let $p = 10u32;
        1u32
    }};
}

pub fn edition_id() -> &'static str {
    "2021"
}

pub fn pat_demo() -> u32 {
    pat_2021_demo!(0 | 1)
}

pub fn pat_param_demo() -> u32 {
    pat_param_2021_demo!(x)
}

#[macro_export]
macro_rules! cross_from_2021 {
    () => {
        2021u32
    };
}

// Edition 2021: IntoIterator for arrays changed (demonstrate edition-sensitive behavior)
pub fn into_iter_demo() -> u32 {
    let arr = [1u32, 2, 3];
    arr.into_iter().sum()
}
