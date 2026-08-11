//! RS-CAN-MAC-002: declarative scope, export, import, re-export, and shadowing.

// Textual ordering demonstration: macro must be defined before use in 2021+
macro_rules! early_macro {
    () => {
        1u32
    };
}

pub fn before_decl_use() -> u32 {
    early_macro!()
}

// Macro defined later, used after
macro_rules! later_macro {
    () => {
        2u32
    };
}

pub fn after_decl_use() -> u32 {
    later_macro!()
}

// Child module resolution: parent macro visible in child via textual scope
#[macro_export]
macro_rules! parent_macro {
    () => {
        10u32
    };
}

pub mod child {
    // child can see parent_macro via crate root export
    pub fn use_parent() -> u32 {
        crate::parent_macro!()
    }

    // qualified path access via crate root
    pub fn via_qualified() -> u32 {
        crate::parent_macro!()
    }
}

// Cross-crate export via decl_provider #[macro_export]
pub fn cross_crate_export() -> u32 {
    decl_provider::scope_demo!()
}

// Re-exported path demonstration
pub use decl_provider::reexported_scope_demo;

pub fn reexport_demo() -> u32 {
    reexported_scope_demo!()
}

// Shadowing: later definition shadows earlier in same module
mod shadowing {
    macro_rules! shadowed {
        () => {
            1u32
        };
    }

    pub fn first() -> u32 {
        shadowed!()
    }

    macro_rules! shadowed {
        () => {
            2u32
        };
    }

    pub fn second() -> u32 {
        shadowed!()
    }
}

// Edition 2015 legacy macro_use import is demonstrated in crates/edition-2015
// which uses `#[macro_use] extern crate decl_provider;`
// Qualified and re-exported paths are shown via `crate::scope::parent_macro!` and `reexported_scope_demo`

// Counterexamples documented:
// - `local_inner_macros` requires internal macro to be marked `local_inner_macros` for cross-macro calls
// - ordering-sensitive validity: using `later_macro!()` before its definition would fail in 2021+
// - same-name imported/textual ambiguity when both a `use` imported macro and textual macro share a name

pub fn scope_summary() -> u32 {
    before_decl_use()
        + after_decl_use()
        + child::use_parent()
        + cross_crate_export()
        + reexport_demo()
        + shadowing::first()
        + shadowing::second()
}
