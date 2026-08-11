#![allow(dead_code)]
use proc_macro::TokenStream;

/// RS-CAN-PROJ-005: procedural-macro dependency role and host universes.
/// Also contributes to RS-CAN-PROJ-014 proc-macro crate type.
/// Function-like proc macro
#[proc_macro]
pub fn make_fn(_input: TokenStream) -> TokenStream {
    "pub fn generated_fn() -> u32 { 42 }".parse().unwrap()
}

// Derive macro stub
#[proc_macro_derive(HelloMacro)]
pub fn hello_macro(_input: TokenStream) -> TokenStream {
    TokenStream::new()
}

// Attribute macro stub
#[proc_macro_attribute]
pub fn my_attr(_attr: TokenStream, item: TokenStream) -> TokenStream {
    item
}
