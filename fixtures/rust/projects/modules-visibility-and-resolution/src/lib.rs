//! Fixture for Rust modules, visibility, and resolution.
//! Covers RS-CAN-MOD-001 through RS-CAN-MOD-014.

// Allow intentionally unused items for fixture demonstration.
#![allow(dead_code)]
#![allow(unused_imports)]

// RS-CAN-MOD-010 extern crate variants.
extern crate alloc;
extern crate fixture_direct as renamed_dep;
extern crate self as mvr_self;

// RS-CAN-MOD-001: inline, name.rs, name/mod.rs, child-directory, #[path] modules with nested children.

// Inline module with nested child.
pub mod inline_root {
    pub fn inline_fn() -> u32 {
        1
    }

    pub mod inline_child {
        pub fn child_fn() -> u32 {
            2
        }

        pub mod inline_grandchild {
            pub fn value() -> u32 {
                3
            }
        }
    }
}

// `name.rs` form.
pub mod standalone_file;

// `name/mod.rs` form.
pub mod legacy_mod;

// `#[path]` mounted with nested children.
#[path = "custom_mapped.rs"]
pub mod custom_mapped;

// cfg-selected module path alternatives on host.
#[cfg(fixture_use_a)]
#[path = "cfg_selected_a.rs"]
pub mod cfg_selected;

#[cfg(not(fixture_use_a))]
#[path = "cfg_selected_b.rs"]
pub mod cfg_selected;

// RS-CAN-MOD-002: one file mounted at two module paths and in two crate roles.
// File `shared_source.rs` mounted twice via `#[path]`.
#[path = "shared_source.rs"]
pub mod shared_first;

#[path = "shared_source.rs"]
pub mod shared_second;

// Also via `include!` producing distinct entity.
pub mod shared_via_include {
    include!("shared_source.rs");
}

// Demonstrate distinct nominal identities.
pub fn demonstrate_shared_distinctness() -> (u32, u32, u32) {
    let a = shared_first::SharedMarker::new(1);
    let b = shared_second::SharedMarker::new(2);
    let c = shared_via_include::SharedMarker::new(3);
    // Types are nominal distinct; assignments between them would fail to compile (documented in counterexamples).
    (a.id, b.id, c.id)
}

// Second crate role mounting same file: binary `src/bin/mvr_bin.rs` also mounts `shared_source.rs`
// via `#[path = "../shared_source.rs"] pub mod bin_shared;` (see that file).

// RS-CAN-MOD-003
pub mod namespaces;

// RS-CAN-MOD-004
pub mod path_roots;

// RS-CAN-MOD-005
pub mod use_forms;

// RS-CAN-MOD-006
pub mod glob_ambiguity;

// RS-CAN-MOD-007
pub mod reexports;

// RS-CAN-MOD-008
pub mod visibility_restricted;

// RS-CAN-MOD-009
pub mod visibility_fields;

// RS-CAN-MOD-010
pub mod extern_prelude;

// RS-CAN-MOD-011
pub mod preludes;

// RS-CAN-MOD-012
pub mod scopes_shadowing;

// RS-CAN-MOD-013
pub mod raw_identifiers;

// RS-CAN-MOD-014
pub mod intra_doc_links;

// Re-export demonstration for downstream cross-crate visibility tests.
pub use reexports::ReexportedDirectType;
pub use reexports::RenamedType as ReexportedRenamed;

/// Fixture summary tying modules together.
pub fn fixture_summary() -> &'static str {
    "modules-visibility-and-resolution"
}

pub fn cfg_selected_summary() -> &'static str {
    cfg_selected::cfg_selected_fn()
}

// Forward reference example re-exported at root.
pub use scopes_shadowing::forward_declared_fn;

// Raw identifier re-exports for cross-edition testing (2015 crate uses old keyword shape).
pub use raw_identifiers::r#try as try_fn;
