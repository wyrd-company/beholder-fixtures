#![allow(dead_code)]

// RS-CAN-MAC-002: legacy macro_use import (edition 2015 style)
#[macro_use]
extern crate decl_provider;

// RS-CAN-MAC-001: 2015 edition fragment grammar demonstration
// In 2015, expr fragment did not yet split expr_2021; this macro uses expr
#[macro_export]
macro_rules! edition_2015_expr {
    ($e:expr) => {
        $e
    };
}

// RS-CAN-MAC-002: cross-crate exported macro via legacy import
pub fn legacy_import_demo() -> &'static str {
    legacy_provider_macro!()
}

pub fn edition_id() -> &'static str {
    "2015"
}

// RS-CAN-MAC-001: expr fragment usage in 2015 edition context
pub fn expr_2015_demo() -> u32 {
    edition_2015_expr!(1 + 2)
}

// Demonstrate that macro defined in 2015 can be invoked from 2024
#[macro_export]
macro_rules! cross_from_2015 {
    () => {
        2015u32
    };
}

// Fragment: pat demonstration pre-2021 (pat matches patterns with |)
#[macro_export]
macro_rules! pat_2015_demo {
    ($p:pat) => {
        match Some(5u32) {
            Some($p) => true,
            _ => false,
        }
    };
}

pub fn pat_demo_value() -> bool {
    pat_2015_demo!(x)
}
