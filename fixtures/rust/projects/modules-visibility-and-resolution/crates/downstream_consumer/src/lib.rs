//! Downstream crate verifying cross-crate visibility boundaries.
//! Only accesses permitted items; private/restricted items are documented as unreachable.

use modules_visibility_and_resolution::visibility_restricted::{PubInRestrictedMod, PublicItem};

use modules_visibility_and_resolution::reexports::ReexportedDirectType;
use modules_visibility_and_resolution::visibility_fields::{MixedStruct, PublicEnum, VisibleTrait};

pub fn downstream_can_access_public() -> u32 {
    let item = PublicItem { value: 10 };
    item.value
}

pub fn downstream_can_access_pub_in_restricted_via_public_type() -> u32 {
    let _ = PubInRestrictedMod { inner: 1 };
    42
}

pub fn downstream_uses_reexported_type() -> ReexportedDirectType {
    ReexportedDirectType::new(7)
}

pub fn downstream_uses_struct_with_public_constructor() -> MixedStruct {
    MixedStruct::new(1, 2)
}

pub fn downstream_matches_public_enum(variant: PublicEnum) -> u32 {
    match variant {
        PublicEnum::PublicVariant(x) => x,
        PublicEnum::PrivatePayloadVariant(_) => 0,
        PublicEnum::UnitVariant => 1,
        PublicEnum::StructVariant { x, y: _ } => x,
    }
}

pub fn downstream_uses_trait(item: &dyn VisibleTrait) -> u32 {
    item.visible_method()
}
