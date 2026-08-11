# Named counterexamples for attributes-and-lints

This document preserves invalid or non-compiled counterexamples beside the valid
demonstrations in source. Only host cfg branches compile in the fixture corpus.

## Invalid attribute position

Outer attributes cannot annotate arbitrary statement positions. The following is
rejected by the compiler and is not present as source:

```rust
#[allow(dead_code)]
let statement_slot = 1;
```

Valid contrast: outer attributes on items, fields, variants, and supported
expression forms appear in `src/attr_positions.rs` and `src/cfg_removal.rs`.

## Unknown tool namespace

Unknown tool namespaces are rejected at compile time. The following is not
present as source:

```rust
#[unknown_tool_namespace::flag]
fn unknown_tool_item() {}
```

Valid contrast: registered tool namespaces `rustfmt::skip` and
`derive_helpers::fixture_tool` appear in `src/attr_positions.rs` and the
`derive_helpers` proc-macro crate.

## `forbid` override failure

A module `forbid` lint cannot be overridden by `allow` on a child item. The
following is not present as source:

```rust
mod forbid_parent {
    #![forbid(unsafe_code)]
    #[allow(unsafe_code)]
    unsafe fn forbidden_override() {}
}
```

Valid contrast: `src/lint_levels.rs` module `forbid_scope` applies
`#![forbid(unsafe_code)]` and documents the override counterexample in comments.

## `cfg!` wrong-platform reference

Code inside a `cfg(windows)` branch is removed on the host linux edge before name
resolution. Referencing windows-only APIs inside that branch fails when the
branch is active. On the host, the branch is absent and the failure does not
occur. The counterexample pattern is:

```rust
#[cfg(windows)]
fn windows_only_reference() {
    let _ = cfg!(windows);
    // windows-only API reference would fail if this branch compiled on host.
}
```

Valid contrast: `cfg!` used in expression positions with host-visible branches
appears in `src/cfg_removal.rs` (`cfg_branch_label`, `cfg_match_arm_label`).
