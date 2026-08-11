// RS-CAN-MOD-005: `use` groups, aliases, self, glob, underscore trait and macro imports, child non-inheritance.

// Source module for imports.
pub mod source {
    pub struct SourceType {
        pub v: u32,
    }

    pub fn source_fn() -> u32 {
        1
    }

    pub const SOURCE_CONST: u32 = 10;

    pub trait SourceTrait {
        fn trait_method(&self) -> u32;
    }

    impl SourceTrait for SourceType {
        fn trait_method(&self) -> u32 {
            self.v
        }
    }

    impl SourceType {
        pub fn inherent_method(&self) -> u32 {
            self.v + 100
        }
    }

    #[macro_export]
    macro_rules! source_macro {
        () => {
            55
        };
    }
}

// Group imports, aliases, `self`, glob, underscore.
pub mod importer {
    // Group: `use source::{a, b}`.
    use crate::use_forms::source::{SOURCE_CONST, SourceType, source_fn};

    // Alias.
    use crate::use_forms::source::SourceType as AliasedType;

    // `self` in import: `{self, Foo}`.
    use crate::use_forms::source::{self, SourceType as DirectType};

    // Glob.
    use crate::use_forms::source::*;

    // Underscore trait import enabling method resolution without naming the trait.
    use crate::use_forms::source::SourceTrait as _;

    // Valid macro import:
    use crate::source_macro;

    pub fn demonstrate_all_forms() -> u32 {
        let t = SourceType { v: 5 };
        let aliased: AliasedType = AliasedType { v: 6 };
        let direct: DirectType = DirectType { v: 7 };
        // Method via underscore import (trait not named locally but method resolves).
        let via_trait = t.trait_method();
        let via_glob = source_fn();
        let via_const = SOURCE_CONST;
        let via_macro = source_macro!();
        // `self` import allows referring to `source` module itself.
        let via_self_mod = self::source_fn();
        // Use glob-imported inherent.
        let via_inherent = t.inherent_method();
        via_trait
            + aliased.v
            + direct.v
            + via_glob
            + via_const
            + via_macro
            + via_self_mod
            + via_inherent
    }

    // Forward item import order-independent (use before declaration).
    // Import with alias to avoid duplicate definition name clash.
    use crate::use_forms::importer::forward_declared_fn as imported_forward;

    pub fn uses_forward_import() -> u32 {
        imported_forward()
    }

    pub fn forward_declared_fn() -> u32 {
        99
    }

    // Child does NOT inherit parent's imports; must re-import.
    pub mod child {
        // This child has no access to parent's `SourceType` import without its own `use`.

        // Must re-import to use.
        use crate::use_forms::source::SourceType;

        pub fn child_needs_own_import() -> SourceType {
            SourceType { v: 10 }
        }

        // Attempt to use parent's `AliasedType` without import would fail (documented in counterexamples).
    }
}

// Re-export helper for demonstrating import shadowing.
pub fn use_forms_summary() -> u32 {
    importer::demonstrate_all_forms()
        + importer::uses_forward_import()
        + importer::child::child_needs_own_import().v
}
