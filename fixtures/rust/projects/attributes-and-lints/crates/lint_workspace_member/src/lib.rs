//! Workspace member inheriting workspace lint tables with a local override.

/// Dead code allowed via member `lints.rust.dead_code = "allow"` override.
#[allow(dead_code)]
fn workspace_member_dead() {}

/// Public summary showing the member compiles under inherited lint tables.
pub fn workspace_member_summary() -> &'static str {
    "lint_workspace_member"
}
