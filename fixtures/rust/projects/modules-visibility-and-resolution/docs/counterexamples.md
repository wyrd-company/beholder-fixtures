# Named counterexamples for modules-visibility-and-resolution

This document preserves invalid or non-compiled counterexamples beside the valid demonstrations. Only checked valid host configurations compile.

## Both candidate module files (RS-CAN-MOD-001)

When `src/standalone_file.rs` exists, `src/standalone_file/mod.rs` must not also exist for the same `mod standalone_file;` declaration. The following layout would be ambiguous and is rejected:

```text
src/standalone_file.rs
src/standalone_file/mod.rs  # duplicate candidate for `mod standalone_file;`
```

Valid contrast: `src/standalone_file.rs` is used for `mod standalone_file;`, while `src/legacy_mod/mod.rs` is the legacy `name/mod.rs` form for a distinct module `legacy_mod`.

## Missing file (RS-CAN-MOD-001)

```rust
mod missing_module; // error: file not found for module `missing_module`
```

Valid contrast: every `mod foo;` in `src/lib.rs` corresponds to an existing file (`standalone_file.rs`, `legacy_mod/mod.rs`, `custom_mapped.rs`, `shared_source.rs`).

## Undeclared file (RS-CAN-MOD-001)

File `src/unlinked.rs` could exist on disk but is not reachable because `lib.rs` never declares `mod unlinked;`. Such a file is not compiled and is not shown here.

## Duplicate binding (RS-CAN-MOD-005)

```rust
use crate::use_forms::source::SourceType;
use crate::use_forms::source::SourceType; // error: duplicate import
```

Valid contrast: `src/use_forms.rs` uses aliasing (`as AliasedType`) and scoped imports to avoid duplication, and imports disjoint names via groups.

## Insufficient re-export visibility (RS-CAN-MOD-007)

```rust
mod private_impl {
    struct PrivateType { v: u32 }
}
pub use crate::private_impl::PrivateType; // error: private type in public re-export (private_interfaces)
```

Valid contrast: `src/reexports.rs` re-exports only `pub` items from `implementation` (`InternalType`), or uses `pub(in ...)`-capped types via a public re-export path (`ReachableCapped`).

## Too-many-`super` path (RS-CAN-MOD-004)

```rust
pub mod a { pub mod b {
    use super::super::super::missing; // error: too many `super` segments beyond crate root
}}
```

Valid contrast: `src/path_roots.rs` demonstrates `super::`, `crate::`, `self::`, and `<Type as Trait>::Assoc` within bounds.

## Illegal underscore import (RS-CAN-MOD-005)

```rust
use crate::use_forms::source::SourceType as _; // error: `SourceType` is a type, not a trait, `as _` only for traits
use crate::use_forms::source::source_fn as _; // error: function not allowed with `as _`
```

Valid contrast: `use crate::use_forms::source::SourceTrait as _;` in `src/use_forms.rs` enables method resolution without naming the trait.

## Broken doc link (RS-CAN-MOD-014)

```rust
/// Link to [`crate::nonexistent::Missing`] // error: unresolved link with deny(warnings) would fail `cargo doc`
pub fn broken_link_demo() {}
```

Valid contrast: `src/intra_doc_links.rs` links only to resolvable items (`crate::reexports::InternalType`, `Self::linked_method`, `crate::reexports::RenamedType`, macro `crate::alpha!`, cross-module type `crate::glob_ambiguity::source_a::CollidingType`) and documents the broken case here.

## Additional invalid module/visibility contrasts

- **Unnameable transitive crate**: `use fixture_transitive::TransitiveType` directly fails because `fixture-transitive` is not a direct dependency of the root crate; valid access is via `fixture_direct::TransitiveType` re-export (`src/extern_prelude.rs`).
- **Private field construction**: `MixedStruct { public_field: 1, private_field: 99, .. }` outside defining module fails; valid construction uses `MixedStruct::new` (`src/visibility_fields.rs`).
- **Glob ambiguity when used**: importing `source_a::*` and `source_b::*` and then using `CollidingType` without disambiguation is ambiguous; valid contrast uses qualified paths `crate::glob_ambiguity::source_a::CollidingType` or explicit `use` shadowing (`src/glob_ambiguity.rs`).
- **Leading `::` edition difference**: `::fixture_direct::DirectType` is legacy absolute path in 2015 vs uniform path in 2018/2024; demonstrated across `crates/edition2015` (requires `extern crate`) and `crates/edition2018` (direct use).
- **Duplicate namespace binding**: declaring `struct Alpha;` and `fn Alpha() {}` in the same value namespace would collide; valid reuse across namespaces (type vs value vs macro) is shown in `src/namespaces.rs`.
- **No-implicit-prelude**: unqualified `Vec` in `#[no_implicit_prelude] mod no_prelude_mod` fails; valid access uses `std::vec::Vec` (`src/preludes.rs`).
