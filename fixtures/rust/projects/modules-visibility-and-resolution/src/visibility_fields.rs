//! RS-CAN-MOD-009: field, constructor, variant, trait-item, impl-item visibility.

pub struct MixedStruct {
    pub public_field: u32,
    pub(crate) crate_field: u32,
    private_field: u32,
}

impl MixedStruct {
    // Public constructor allowing creation despite private fields.
    pub fn new(public: u32, crate_f: u32) -> Self {
        Self {
            public_field: public,
            crate_field: crate_f,
            private_field: 99,
        }
    }

    pub fn new_with_private(public: u32, crate_f: u32, private: u32) -> Self {
        Self {
            public_field: public,
            crate_field: crate_f,
            private_field: private,
        }
    }

    pub fn read_private(&self) -> u32 {
        self.private_field
    }
}

// Tuple struct with mixed visibility.
pub struct TupleMixed(pub u32, pub(crate) u32, u32);

impl TupleMixed {
    pub fn new(a: u32, b: u32, c: u32) -> Self {
        Self(a, b, c)
    }

    pub fn values(&self) -> (u32, u32, u32) {
        (self.0, self.1, self.2)
    }
}

impl TupleMixed {
    // Demonstrate external construction via tuple constructor requires all fields visible.
    // Since fields 1 and 2 are crate-private/private, downstream cannot use `TupleMixed(1,2,3)` directly,
    // must use `TupleMixed::new`.
    pub fn constructible_via_new() -> Self {
        Self::new(1, 2, 3)
    }
}

// Enum with variant visibility nuances.
pub enum PublicEnum {
    PublicVariant(u32),
    PrivatePayloadVariant(u32),
    UnitVariant,
    StructVariant { x: u32, y: u32 },
}

// Enum `#[non_exhaustive]` comparison with privacy.
#[non_exhaustive]
pub enum NonExhaustiveEnum {
    Known(u32),
    Hidden(u32),
}

// Trait where items follow trait container visibility; `pub` on trait items is not permitted
// outside inherent? Actually trait items inherent visibility is determined by trait visibility.
pub trait VisibleTrait {
    fn visible_method(&self) -> u32;

    fn default_method(&self) -> u32 {
        100
    }
}

impl VisibleTrait for MixedStruct {
    fn visible_method(&self) -> u32 {
        self.public_field
    }
}

// Inherent impl with public/private methods - impl visibility is per-item.
pub struct InherentDemo {
    pub v: u32,
}

impl InherentDemo {
    pub fn public_method(&self) -> u32 {
        self.v
    }

    pub(crate) fn crate_method(&self) -> u32 {
        self.v + 1
    }

    fn private_method(&self) -> u32 {
        self.v + 2
    }

    pub fn calls_private(&self) -> u32 {
        self.private_method()
    }
}

// Cross-crate field update restrictions demonstration.
// External struct update syntax `MixedStruct { public_field: 1, ..other }` fails if private fields are required to be filled
// without visible path - downstream must use constructor.
pub fn use_struct_literal_within_crate() -> MixedStruct {
    // Within crate, all fields accessible, struct literal allowed even with private fields via direct same-module construction.
    MixedStruct {
        public_field: 10,
        crate_field: 20,
        private_field: 30,
    }
}

pub fn cross_crate_construction_demo() -> MixedStruct {
    // Public constructor works downstream.
    MixedStruct::new(5, 6)
}

pub fn tuple_constructor_in_crate() -> TupleMixed {
    TupleMixed(1, 2, 3)
}
