// RS-CAN-MOD-008: private, pub(self), pub(super), pub(crate), pub(in path), pub boundaries.

pub struct VisibilityDemo {
    private_field: u32,
    pub public_field: u32,
    pub(crate) crate_field: u32,
    pub(super) super_field: u32,
    pub(self) self_field: u32,
}

impl VisibilityDemo {
    pub fn new() -> Self {
        Self {
            private_field: 1,
            public_field: 2,
            crate_field: 3,
            super_field: 4,
            self_field: 5,
        }
    }

    pub fn read_private(&self) -> u32 {
        self.private_field
    }
}

struct PrivateItem {
    value: u32,
}

pub(self) struct SelfVisible {
    pub value: u32,
}

pub(super) struct SuperVisible {
    pub value: u32,
}

pub(crate) struct CrateVisible {
    pub crate_value: u32,
}

pub(in crate::visibility_restricted) struct PubInRestricted {
    pub inner: u32,
}

pub mod inner_mod {
    use crate::visibility_restricted::PubInRestricted;

    pub(in crate::visibility_restricted) struct PubInModuleVisible {
        pub inner: u32,
    }

    pub fn inner_user() -> PubInRestricted {
        PubInRestricted { inner: 10 }
    }

    pub fn make_visible() -> PubInModuleVisible {
        PubInModuleVisible { inner: 11 }
    }

    pub mod child {
        use crate::visibility_restricted::SuperVisible;

        pub fn child_can_access_super() -> SuperVisible {
            SuperVisible { value: 20 }
        }

        pub fn child_can_access_pub_in_parent() -> super::PubInModuleVisible {
            super::PubInModuleVisible { inner: 30 }
        }

        // Child defines pub(super) item visible to its parent `inner_mod`.
        pub(super) struct ChildSuperVisible {
            pub v: u32,
        }
    }

    // Parent (inner_mod) can access child's pub(super) item.
    pub fn parent_accesses_child_super() -> u32 {
        child::ChildSuperVisible { v: 31 }.v
    }
}

pub fn same_crate_can_access_pub_in() -> PubInRestricted {
    PubInRestricted { inner: 40 }
}

pub struct PublicItem {
    pub value: u32,
}

pub(crate) struct PubCrateOnly {
    pub v: u32,
}

pub(super) struct PubSuperOnly {
    pub v: u32,
}

pub mod restricted_paths {
    pub(in crate::visibility_restricted) struct RestrictedA {
        pub v: u32,
    }

    pub(crate) struct RestrictedCrate {
        pub v: u32,
    }
}

// Effective visibility: nominal `pub` capped by private container `private_container`.
// `private_container` is private, so `CappedPublic` nominally `pub` is not reachable outside `visibility_restricted` except via re-export.
mod private_container {
    pub struct CappedPublic {
        pub v: u32,
    }

    pub fn capped_fn() -> u32 {
        99
    }
}

// Re-export to make capped item reachable downstream via public path; original `private_container::CappedPublic` remains private.
pub use crate::visibility_restricted::private_container::CappedPublic as ReachableCapped;

pub struct PubInModuleVisible {
    pub inner: u32,
}

pub struct PubInRestrictedMod {
    pub inner: u32,
}

// Sibling demonstration: two sibling modules inside `visibility_restricted`.
pub mod sibling_a {
    pub(crate) struct SiblingCrateVisible {
        pub v: u32,
    }
    pub(self) struct SiblingSelfVisible {
        pub v: u32,
    }
}

pub mod sibling_b {
    // Sibling `sibling_b` can access `sibling_a::SiblingCrateVisible` because it's `pub(crate)`, but not `SiblingSelfVisible` (`pub(self)`).
    use crate::visibility_restricted::sibling_a::SiblingCrateVisible;

    pub fn sibling_accesses_crate_visible() -> SiblingCrateVisible {
        SiblingCrateVisible { v: 10 }
    }

    // `SiblingCrateVisible` via `crate::` path demonstrates same-crate access from sibling.
    pub fn sibling_via_crate_path() -> crate::visibility_restricted::CrateVisible {
        crate::visibility_restricted::CrateVisible { crate_value: 11 }
    }
}

// Child/sibling/parent helpers correctly located.
pub fn child_access_demo() -> u32 {
    crate::visibility_restricted::inner_mod::parent_accesses_child_super()
}

pub fn sibling_access_demo_via_crate() -> CrateVisible {
    // This function is inside `visibility_restricted` (defining module) – for true sibling, see `sibling_b::sibling_accesses_crate_visible`.
    // Same-crate access via `crate::` path from within crate, but outside strict `pub(self)` boundary.
    CrateVisible { crate_value: 2 }
}

// Parent access: function in parent (`visibility_restricted`) accessing child's `pub(super)` – already via `parent_accesses_child_super`.

// Same-crate access from outside `visibility_restricted` – demonstrate in `crate::visibility_restricted::CrateVisible` accessible via `crate::` from any sibling crate module.
// The `sibling_b` module above already demonstrates same-crate sibling access; downstream crate `fixture-downstream` demonstrates cross-crate `pub` only.

// Original helpers kept for compatibility, now with proper allowances.
pub fn sibling_access_demo() -> u32 {
    // Inside defining module, `SelfVisible` (`pub(self)`) is accessible; from sibling it would be inaccessible – documented as valid same-module vs sibling distinction.
    let s = SelfVisible { value: 1 };
    let c = CrateVisible { crate_value: 2 };
    s.value + c.crate_value
}

pub fn parent_accesses_super() -> SuperVisible {
    SuperVisible { value: 50 }
}

// Effective visibility helper: downstream can only reach `ReachableCapped`, not `private_container::CappedPublic` directly.
pub fn effective_visibility_demo() -> ReachableCapped {
    ReachableCapped { v: 60 }
}
