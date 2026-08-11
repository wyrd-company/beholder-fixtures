//! RS-CAN-MOD-004: crate, self, super, leading ::, Self, extern-prelude path roots.

// Local module named like a dependency to test shadowing and disambiguation.
pub mod fixture_direct {
    pub struct LocalShadow {
        pub v: u32,
    }

    impl LocalShadow {
        pub fn new(v: u32) -> Self {
            Self { v }
        }
    }

    pub fn local_fn() -> u32 {
        100
    }
}

pub struct PathRootDemo {
    pub value: u32,
}

impl PathRootDemo {
    pub fn new(v: u32) -> Self {
        Self { value: v }
    }

    // `Self` as path root / constructor.
    pub fn via_self(v: u32) -> Self {
        Self { value: v }
    }

    pub fn via_self_associated() -> u32 {
        Self::associated_fn()
    }

    pub fn associated_fn() -> u32 {
        200
    }
}

pub mod outer {
    pub mod inner {
        // `super::` goes to outer.
        pub fn via_super() -> u32 {
            super::outer_fn()
        }

        // `self::` refers to current module.
        pub fn via_self_path() -> u32 {
            self::inner_fn()
        }

        pub fn inner_fn() -> u32 {
            300
        }

        // `crate::` rooted at crate root.
        pub fn via_crate() -> u32 {
            crate::path_roots::outer::outer_fn()
        }
    }

    pub fn outer_fn() -> u32 {
        301
    }

    // `crate::` from outer as well.
    pub fn via_crate_direct() -> u32 {
        crate::path_roots::PathRootDemo::associated_fn()
    }
}

// Extern prelude root: `fixture_direct` crate vs local `crate::path_roots::fixture_direct`
pub fn extern_prelude_vs_local() -> (u32, u32) {
    // Local shadow:
    let local = crate::path_roots::fixture_direct::LocalShadow::new(1);
    // Extern prelude via absolute `::` (legacy) or via extern prelude name directly.
    // In edition 2024, `fixture_direct::DirectType` resolves via extern prelude.
    let external = ::fixture_direct::DirectType::new(2);
    // Also `crate::` would be wrong for external; must use extern root.
    (local.v, external.value)
}

// Fully qualified syntax: `<Type as Trait>::Item` and associated-type traversal.
pub trait PathTrait {
    type Assoc;
    fn trait_fn() -> u32;
}

impl PathTrait for PathRootDemo {
    type Assoc = u32;
    fn trait_fn() -> u32 {
        400
    }
}

pub fn qualified_path_demo() -> u32 {
    <PathRootDemo as PathTrait>::trait_fn()
}

// `Self` constructor demonstration inside impl.
pub fn self_constructor_demo() -> PathRootDemo {
    PathRootDemo::via_self(500)
}
