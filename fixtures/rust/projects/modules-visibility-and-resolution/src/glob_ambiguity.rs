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

    pub struct Option(pub u32);

    macro_rules! shared_macro {
        () => {
            100
        };
    }
    pub(crate) use shared_macro;

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

    pub struct Option(pub u32);

    macro_rules! shared_macro {
        () => {
            200
        };
    }
    pub(crate) use shared_macro;

    #[macro_export]
    macro_rules! colliding_macro_b {
        () => {
            200
        };
    }
}

pub mod glob_user_unused {
    use crate::glob_ambiguity::source_a::*;
    use crate::glob_ambiguity::source_b::*;

    pub fn non_colliding_use() -> u32 {
        42
    }
}

pub mod glob_user_shadowed {
    use crate::glob_ambiguity::source_a::*;
    use crate::glob_ambiguity::source_b::*;

    pub fn explicit_resolution_a() -> crate::glob_ambiguity::source_a::CollidingType {
        crate::glob_ambiguity::source_a::CollidingType { v: 1 }
    }

    pub fn explicit_resolution_b() -> crate::glob_ambiguity::source_b::CollidingType {
        crate::glob_ambiguity::source_b::CollidingType { v: 2 }
    }

    pub fn colliding_fn_a() -> u32 {
        crate::glob_ambiguity::source_a::colliding_fn()
    }

    pub fn colliding_fn_b() -> u32 {
        crate::glob_ambiguity::source_b::colliding_fn()
    }

    pub mod shadow_via_explicit {
        use crate::glob_ambiguity::source_a::CollidingType as ExplicitType;
        use crate::glob_ambiguity::source_a::*;
        use crate::glob_ambiguity::source_b::*;

        pub fn uses_shadowed_type() -> ExplicitType {
            ExplicitType { v: 5 }
        }
    }

    pub mod shadow_via_local {
        use crate::glob_ambiguity::source_a::*;
        use crate::glob_ambiguity::source_b::*;

        pub struct CollidingType {
            pub local: u32,
        }

        pub fn uses_local_shadow() -> CollidingType {
            CollidingType { local: 5 }
        }
    }
}

pub mod public_glob_exporter {
    pub use crate::glob_ambiguity::source_a::*;

    pub fn exported_const_user() -> u32 {
        COLLIDING_CONST
    }
}

pub mod prelude_glob_shadow {
    use crate::glob_ambiguity::source_a::*;

    pub fn shadowed_prelude_via_glob() -> Option {
        Option(10)
    }

    pub fn std_option_still_accessible_via_path() -> std::option::Option<u32> {
        None
    }
}

pub mod enum_glob_collision {
    pub use crate::glob_ambiguity::source_a::CollidingEnum::*;

    pub fn uses_imported_variant() -> crate::glob_ambiguity::source_a::CollidingEnum {
        VariantA
    }

    pub fn explicit_variant_a() -> crate::glob_ambiguity::source_a::CollidingEnum {
        crate::glob_ambiguity::source_a::CollidingEnum::VariantA
    }

    pub fn explicit_variant_b() -> crate::glob_ambiguity::source_b::CollidingEnum {
        crate::glob_ambiguity::source_b::CollidingEnum::VariantB
    }

    pub mod via_b {
        pub use crate::glob_ambiguity::source_b::CollidingEnum::*;

        pub fn variant_b() -> crate::glob_ambiguity::source_b::CollidingEnum {
            VariantB
        }
    }

    // Documented collision: `use source_a::CollidingEnum::*; use source_b::CollidingEnum::*;` then `VariantA` ambiguous – must use qualified `source_a::...::VariantA`.
}

pub mod macro_glob_collision {
    // `shared_macro` is `pub use` re-exported macro_rules in each source; glob import would make `shared_macro!()` ambiguous.
    // Valid single-source glob:
    use crate::glob_ambiguity::source_a::shared_macro;

    pub fn macro_via_a() -> u32 {
        shared_macro!()
    }

    pub fn macro_a_explicit() -> u32 {
        crate::glob_ambiguity::source_a::shared_macro!()
    }

    pub fn macro_b_explicit() -> u32 {
        crate::glob_ambiguity::source_b::shared_macro!()
    }

    pub fn distinct_macros_via_crate() -> u32 {
        crate::colliding_macro_a!() + crate::colliding_macro_b!()
    }
}

pub mod prelude_interaction_alias {
    use crate::glob_ambiguity::source_a::CollidingType as Option;

    pub fn shadowed_prelude_alias() -> Option {
        Option { v: 10 }
    }
}

pub fn glob_summary() -> u32 {
    glob_user_unused::non_colliding_use()
        + glob_user_shadowed::shadow_via_local::uses_local_shadow().local
        + glob_user_shadowed::explicit_resolution_a().v
        + glob_user_shadowed::explicit_resolution_b().v
        + public_glob_exporter::exported_const_user()
        + prelude_glob_shadow::shadowed_prelude_via_glob().0
}
