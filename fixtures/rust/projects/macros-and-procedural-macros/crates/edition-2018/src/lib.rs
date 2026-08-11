#![allow(dead_code)]

// RS-CAN-MAC-002: uniform paths (2018+) vs legacy extern crate
// In 2018+, `use decl_provider::fragment_demo;` works without extern crate
use decl_provider::fragment_demo;
use edition_2015::edition_id as edition_2015_id;

pub fn edition_id() -> &'static str {
    "2018"
}

pub fn uniform_path_demo() -> &'static str {
    edition_2015_id()
}

pub fn fragment_via_uniform_path() -> &'static str {
    fragment_demo!(ident sample)
}

// RS-CAN-MAC-001: block and stmt fragments in 2018 edition
#[macro_export]
macro_rules! edition_2018_macro {
    ($b:block) => {
        $b
    };
    ($s:stmt) => {
        $s
    };
}

pub fn block_demo() -> u32 {
    edition_2018_macro!({ 5 + 5 })
}

#[macro_export]
macro_rules! cross_from_2018 {
    () => {
        2018u32
    };
}
