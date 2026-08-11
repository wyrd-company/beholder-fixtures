// RS-CAN-MOD-006: glob ambiguity, shadowing, public glob re-export.

pub mod source_a {
    pub struct CollidingType {
        pub v: u32,
    }

    pub fn colliding_fn() -> u32 {
        1
    }

    pub const COLLIDING_CONST: u32 = 10;

    pub enum CollidingEnum {
        VariantA,
        VariantB,
    }

    #[macro_export]
    macro_rules! colliding_macro_a {
        () => {
            100
        };
    }
}

pub mod source_b {
    pub struct CollidingType {
        pub v: u32,
    }

    pub fn colliding_fn() -> u32 {
        2
    }

    pub const COLLIDING_CONST: u32 = 20;

    pub enum CollidingEnum {
        VariantA,
        VariantB,
    }

    #[macro_export]
    macro_rules! colliding_macro_b {
        () => {
            200
        };
    }
}

// Two colliding globs; only when the colliding name is used does ambiguity surface.
pub mod glob_user_unused {
    use crate::glob_ambiguity::source_a::*;
    use crate::glob_ambiguity::source_b::*;

    // Not using colliding names here: no ambiguity error while unused.
    pub fn non_colliding_use() -> u32 {
        42
    }
}

// Explicit shadowing resolves ambiguity: explicit import shadows globs.
pub mod glob_user_shadowed {
    use crate::glob_ambiguity::source_a::*;
    use crate::glob_ambiguity::source_b::*;

    // To demonstrate explicit shadowing, use qualified paths instead of ambiguous glob names.
    // Separate helper for explicit type via fully qualified path.
    pub fn explicit_resolution_a() -> crate::glob_ambiguity::source_a::CollidingType {
        crate::glob_ambiguity::source_a::CollidingType { v: 1 }
    }

    pub fn explicit_resolution_b() -> crate::glob_ambiguity::source_b::CollidingType {
        crate::glob_ambiguity::source_b::CollidingType { v: 2 }
    }

    // Function collision resolved explicitly.
    pub fn colliding_fn_a() -> u32 {
        crate::glob_ambiguity::source_a::colliding_fn()
    }

    pub fn colliding_fn_b() -> u32 {
        crate::glob_ambiguity::source_b::colliding_fn()
    }

    // Explicit import shadowing in a dedicated submodule.
    pub mod shadow_via_explicit {
        use crate::glob_ambiguity::source_a::*;
        use crate::glob_ambiguity::source_b::*;
        // Explicit import shadows glob ambiguity for this name.
        use crate::glob_ambiguity::source_a::CollidingType as ExplicitType;

        pub fn uses_shadowed_type() -> ExplicitType {
            ExplicitType { v: 5 }
        }
    }

    // Local definition shadowing in another dedicated submodule.
    pub mod shadow_via_local {
        use crate::glob_ambiguity::source_a::*;
        use crate::glob_ambiguity::source_b::*;

        pub struct CollidingType {
            pub local: u32,
        }

        // The local definition shadows the glob-imported `CollidingType`.
        pub fn uses_local_shadow() -> CollidingType {
            CollidingType { local: 5 }
        }
    }
}

// Public glob re-export.
pub mod public_glob_exporter {
    // Public glob re-export: downstream sees these names via this module.
    pub use crate::glob_ambiguity::source_a::*;

    pub fn exported_const_user() -> u32 {
        COLLIDING_CONST
    }
}

// Interaction with prelude: glob-imported `Option` vs prelude `Option` - local wins when shadowed.
pub mod prelude_interaction {
    use crate::glob_ambiguity::source_a::CollidingType as Option;

    // `Option` here refers to `CollidingType` locally shadowing `core::option::Option` prelude.
    pub fn shadowed_prelude() -> Option {
        Option { v: 10 }
    }
}

// Enum variant glob import ambiguity nuance.
pub mod enum_glob {
    pub use crate::glob_ambiguity::source_a::CollidingEnum::*;
    // Variant `VariantA` now directly nameable.

    pub fn uses_imported_variant() -> crate::glob_ambiguity::source_a::CollidingEnum {
        VariantA
    }
}

// Macro namespace glob behavior distinguished.
pub mod macro_glob {
    // Macros are in macro namespace; glob import may be separate.
    use crate::colliding_macro_a;

    pub fn macro_use() -> u32 {
        colliding_macro_a!()
    }
}

pub fn glob_summary() -> u32 {
    glob_user_unused::non_colliding_use()
        + glob_user_shadowed::shadow_via_local::uses_local_shadow().local
        + glob_user_shadowed::explicit_resolution_a().v
        + glob_user_shadowed::explicit_resolution_b().v
        + public_glob_exporter::exported_const_user()
}
