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

// Private item - only crate::visibility_restricted::* inner can access.
struct PrivateItem {
    value: u32,
}

// pub(self) - visible only within this module.
pub(self) struct SelfVisible {
    pub value: u32,
}

// pub(super) - visible to parent module (crate root via `visibility_restricted` parent).
pub(super) struct SuperVisible {
    pub value: u32,
}

// pub(crate) - visible throughout crate, not downstream.
pub(crate) struct CrateVisible {
    pub crate_value: u32,
}

// pub(in path) - visible within ancestor `crate`.
pub(in crate::visibility_restricted) struct PubInRestricted {
    pub inner: u32,
}

pub mod inner_mod {
    use crate::visibility_restricted::PubInRestricted;

    // Visible within `crate::visibility_restricted`.
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
    }
}

// Use `pub(in crate::visibility_restricted)` from outside demonstrates same-crate access.
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

// Alias for checklist mapping - re-use same structs with alternative names for coverage.
pub mod restricted_paths {
    pub(in crate::visibility_restricted) struct RestrictedA {
        pub v: u32,
    }

    pub(crate) struct RestrictedCrate {
        pub v: u32,
    }
}

// Effective visibility: nominal `pub` capped by private container.
pub mod private_container {
    pub struct CappedPublic {
        pub v: u32,
    }
}

// Re-export to make capped item reachable downstream via public path.
pub use crate::visibility_restricted::private_container::CappedPublic as ReachableCapped;

pub struct PubInModuleVisible {
    pub inner: u32,
}

pub struct PubInRestrictedMod {
    pub inner: u32,
}

// Same-crate access helpers.
pub fn sibling_access_demo() -> u32 {
    let s = SelfVisible { value: 1 };
    let c = CrateVisible { crate_value: 2 };
    s.value + c.crate_value
}

pub fn parent_accesses_super() -> SuperVisible {
    SuperVisible { value: 50 }
}
