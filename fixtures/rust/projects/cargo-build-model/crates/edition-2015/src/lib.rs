#![allow(dead_code)]
//! RS-CAN-PROJ-016: edition 2015 sensitive constructs and cross-edition macro.
//! Uses `extern crate` (2015 style) and `try!` macro.

#[macro_export]
macro_rules! cross_edition_macro {
    () => {
        2015
    };
}

pub fn edition_id() -> &'static str {
    "2015"
}

// 2015 macro fragment: try! was idiomatic.
#[allow(deprecated)]
pub fn try_macro_demo() -> Result<u32, &'static str> {
    let v: Result<u32, &'static str> = Ok(1);
    let x = try!(v);
    Ok(x)
}

// Raw identifier example (raw identifiers stabilized later but usable via r#)
#[allow(clippy::let_and_return)]
pub fn raw_ident_demo() -> u32 {
    let r#type = 42;
    r#type
}
