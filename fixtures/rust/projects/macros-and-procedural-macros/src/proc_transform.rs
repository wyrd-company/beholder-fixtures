//! RS-CAN-MAC-005 and MAC-006: derive usage and procedural transformation.

// RS-CAN-MAC-005: derive with helper attributes over generic input
use macro_host::Describe;

#[derive(Describe)]
#[describe(tag = "demo_tag")]
pub struct DemoStruct {
    pub field: u32,
}

#[derive(Describe)]
#[describe(tag = "generic_tag")]
pub struct GenericDemo<T> {
    pub inner: T,
}

#[derive(Describe)]
pub struct NoTagStruct {
    pub x: u32,
}

// Consumed through bound in derive_support::consume_describe
pub fn derive_demo() -> String {
    let d = DemoStruct { field: 1 };
    let g = GenericDemo { inner: 42u32 };
    let n = NoTagStruct { x: 5 };
    let a = crate::derive_support::consume_describe(&d);
    let b = crate::derive_support::consume_describe(&g);
    let c = crate::derive_support::consume_describe(&n);
    format!("{a}|{b}|{c}")
}

// RS-CAN-MAC-006: attribute and function-like procedural transformation

// Attribute producing item output (wrap_fn preserves function and adds marker)
#[macro_host::wrap_fn]
pub fn wrapped_function(x: u32) -> u32 {
    x + 1
}

// Attribute preserving/removing variant
#[macro_host::transform_item]
pub fn preserved_function(x: u32) -> u32 {
    x * 2
}

// Inline module transformation via attribute
#[macro_host::transform_item]
pub mod transformed_mod {
    pub fn mod_fn() -> u32 {
        10
    }
}

// Function-like producing item and expression output
pub fn proc_item_usage() -> u32 {
    // make_item generates struct
    macro_host::make_item!(TransformGenerated);
    let t = TransformGenerated { value: 3 };
    t.get()
}

pub fn proc_expr_usage() -> u32 {
    macro_host::make_expr!() // expands to 42
}

// Reference generated entities from ordinary code
pub fn transform_demo() -> u32 {
    wrapped_function(5)
        + preserved_function(3)
        + transformed_mod::mod_fn()
        + proc_item_usage()
        + proc_expr_usage()
}

// Built-in derives for comparison (Debug etc from MAC-005)
#[derive(Debug, Clone)]
pub struct ClonedDemo {
    pub v: u32,
}

pub fn proc_transform_summary() -> String {
    let d = derive_demo();
    let t = transform_demo();
    format!("{d}:{t}")
}
