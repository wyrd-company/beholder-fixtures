//! Private API surface for RS-CAN-TEST-001.
//! Items here are visible inside the crate but not to external integration tests.

pub(crate) fn private_helper() -> u32 {
    7
}

pub(crate) fn private_const_value() -> u32 {
    PRIVATE_CONST
}

const PRIVATE_CONST: u32 = 7;

pub(crate) struct PrivateType {
    pub(crate) value: u32,
}

pub(crate) fn private_type_value(item: &PrivateType) -> u32 {
    item.value
}
