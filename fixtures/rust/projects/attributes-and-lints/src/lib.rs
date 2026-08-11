//! Fixture demonstrating Rust attribute and lint surface for code-graph evaluation.

#![warn(missing_docs)]
// Intentional derive output is not fixture-authored documentation.
#![allow(missing_docs)]
#![warn(unfulfilled_lint_expectations)]

mod attr_positions;
mod cfg_removal;
mod diagnostic_attrs;
mod lint_levels;
mod target_cfg;

pub use attr_positions::{DemoDeriveStruct, DocDemo, ReprDemo, ToolDemo, attribute_summary};
pub use cfg_removal::{CfgEnum, CfgStruct, cfg_branch_label};
pub use diagnostic_attrs::{
    codegen_hint_summary, cross_crate_summary, deprecated_call_site, must_use_call_site,
    track_caller_site,
};
pub use lint_levels::{LintScopeDemo, lint_scope_summary};
pub use target_cfg::{custom_cfg_label, target_family_summary};

/// Project-level summary tying attribute and lint modules together.
pub fn fixture_summary() -> &'static str {
    "attributes-and-lints"
}
