// RS-CAN-MOD-005: `use` groups, aliases, self, glob, underscore trait and macro imports, child non-inheritance.

// Source module for imports.
pub mod source {
    pub struct SourceType {
        pub v: u32,
    }

    // Tuple struct provides both type and value (constructor) bindings on import – multi-namespace.
    pub struct TupleSource(pub u32);

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

    impl SourceTrait for TupleSource {
        fn trait_method(&self) -> u32 {
            self.0
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

    // Additional macro for underscore import demonstration (same macro, different import style)
    #[macro_export]
    macro_rules! another_macro {
        () => {
            56
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

    // Underscore macro import (valid) – brings macro into scope without introducing a name binding.
    use crate::source_macro as _;

    // Valid named macro import (also shown for contrast, in separate scope below).
    use crate::another_macro;

    // Multi-namespace import: `TupleSource` is tuple struct, so `use` brings both type and value (constructor).
    use crate::use_forms::source::TupleSource;

    pub fn demonstrate_all_forms() -> u32 {
        let t = SourceType { v: 5 };
        let aliased: AliasedType = AliasedType { v: 6 };
        let direct: DirectType = DirectType { v: 7 };
        // Method via underscore trait import (trait not named locally but method resolves).
        let via_trait = t.trait_method();
        // TupleSource used as type and as value constructor (multi-namespace)
        let tuple_val: TupleSource = TupleSource(8);
        let tuple_trait = tuple_val.trait_method();
        let via_glob = source_fn();
        let via_const = SOURCE_CONST;
        // Macro via underscore import (`source_macro as _` already imported above, usable via crate path)
        let via_underscore_macro = crate::source_macro!();
        // Named macro import
        let via_named_macro = another_macro!();
        // `self` import allows referring to `source` module itself.
        let via_self_mod = self::source_fn();
        // Use glob-imported inherent.
        let via_inherent = t.inherent_method();
        via_trait
            + aliased.v
            + direct.v
            + via_glob
            + via_const
            + via_underscore_macro
            + via_named_macro
            + via_self_mod
            + via_inherent
            + tuple_trait
            + tuple_val.0
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

        // Underscore imports also not inherited – demonstrated separately.
        // `SourceTrait as _` from parent not visible here; need own `use crate::use_forms::source::SourceTrait as _;` to enable trait method.
        pub fn child_underscore_not_inherited() -> u32 {
            use crate::use_forms::source::SourceTrait as _;
            let t = SourceType { v: 5 };
            t.trait_method()
        }

        // Attempt to use parent's `AliasedType` without import would fail (documented in counterexamples).
    }

    // Separate module demonstrating underscore macro import alone, to avoid duplicate binding conflict.
    pub mod underscore_macro_demo {
        use crate::another_macro as _;
        use crate::source_macro as _;

        pub fn uses_underscore_macros() -> u32 {
            crate::source_macro!() + crate::another_macro!()
        }
    }
}

// Re-export helper for demonstrating import shadowing.
pub fn use_forms_summary() -> u32 {
    importer::demonstrate_all_forms()
        + importer::uses_forward_import()
        + importer::child::child_needs_own_import().v
        + importer::underscore_macro_demo::uses_underscore_macros()
}
