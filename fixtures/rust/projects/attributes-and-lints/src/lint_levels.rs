//! Lint levels, scopes, expectations, and configuration surfaces.

/// Crate-visible lint scope summary.
pub fn lint_scope_summary() -> &'static str {
    let _ = deny_scope::deny_scope_live();
    "lint_levels"
}

/// Demonstration struct for item-scope lint attributes.
pub struct LintScopeDemo {
    /// Field with item lint allow.
    #[allow(dead_code)]
    pub allowed_dead_field: i32,
}

/// Module with inner lint attributes at module scope.
pub mod module_lint_scopes {
    #![allow(unused_variables)]
    #![warn(dead_code)]

    /// Item with allow lint overriding module warn for this item.
    #[allow(dead_code)]
    fn item_allowed_dead() {}

    /// Item with warn lint on unused variable.
    #[warn(unused_variables)]
    pub fn item_warn_unused() {
        let unused_slot = 1;
        let _ = unused_slot;
        let never_read = 2;
        let _ = never_read;
    }

    /// Fulfilled `expect` lint on dead code.
    #[expect(dead_code)]
    fn fulfilled_expect_dead() {}

    /// Unfulfilled `expect` lint retained for `unfulfilled_lint_expectations` warning.
    #[expect(dead_code)]
    pub fn unfulfilled_expect_live() -> i32 {
        42
    }
}

/// Module with forbid lint at module scope.
pub mod forbid_scope {
    #![forbid(unsafe_code)]

    /// Safe function inside forbid(unsafe_code) module.
    pub fn safe_only() -> i32 {
        1
    }

    // Counterexample (invalid, not compiled): `#[allow(unsafe_code)] unsafe fn bad() {}` cannot override module `forbid`.
}

/// Module with deny lint at module scope for dead code.
pub mod deny_scope {
    #![deny(dead_code)]

    /// Live function proving deny scope compiles when code is used.
    pub fn deny_scope_live() -> i32 {
        9
    }
}

/// Item-scope deny lint on a live function with no violations.
#[deny(unused_variables)]
pub fn deny_unused_variables_ok() -> i32 {
    let used = 3;
    let _ = used;
    used
}

// Workspace lint inheritance is demonstrated by `lint_workspace_member` compiling with workspace `dead_code = "warn"` overridden to `allow` in the member manifest.
// Command-line deny (`-D dead_code` via `fixture-lint-deny` on helper packages) and cap (`fixture-lint-cap`) are exercised by Taskfile aliases.
