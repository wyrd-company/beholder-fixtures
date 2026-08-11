//! Inner, outer, active, inert, helper, and tool attributes.

use derive_helpers::DemoDerive;

/// Outer documentation with alias attribute.
#[doc(alias = "AttributeSummary")]
pub fn attribute_summary() -> &'static str {
    "attr_positions"
}

/// Outer `repr` attribute on a struct.
#[repr(C)]
pub struct ReprDemo {
    /// Field with outer lint attribute.
    #[allow(dead_code)]
    pub field: u8,
}

/// Outer derive with helper attribute on the type.
#[derive(DemoDerive)]
#[demo_helper(note = "helper on derive input")]
pub struct DemoDeriveStruct {
    /// Variant-style field attribute slot on a struct field.
    #[doc = "field doc via outer attribute"]
    pub slot: i32,
}

/// Registered tool namespace item via proc-macro attribute.
#[derive_helpers::fixture_tool]
pub fn tool_namespace_item() -> &'static str {
    "fixture_tool_namespace"
}

/// Outer doc and tool attributes on an item.
#[derive(Debug, Clone, Copy)]
#[rustfmt::skip]
pub struct ToolDemo {
  /// Inert outer attribute on a field.
  #[allow(unused)]
  pub marker: bool,
}

/// Module demonstrating crate and module inner attributes.
#[allow(clippy::mixed_attributes_style)]
pub mod inner_attr_module {
    //! Module outer doc comment desugars to an inner doc attribute.
    #![doc = "module inner doc attribute"]
    #![allow(unused_variables)]

    /// Item inside a module with inner attributes applied above.
    pub fn module_inner_summary() -> &'static str {
        "inner_attr_module"
    }
}

/// Outer `doc` attribute on a struct.
#[doc = "DocDemo outer doc attribute"]
pub struct DocDemo;

/// Counterexample (invalid, not compiled): outer attribute on a statement position.
/// `#[allow(dead_code)] let x = 1;` is rejected because statements lack outer attributes.
pub struct CounterexampleDocs;

// Counterexample (invalid, not compiled): unknown tool namespace `#[unknown_tool::flag]`.
// Counterexample (invalid, not compiled): `#[forbid(unsafe_code)]` cannot be overridden by `#[allow(unsafe_code)]` on a child item.
