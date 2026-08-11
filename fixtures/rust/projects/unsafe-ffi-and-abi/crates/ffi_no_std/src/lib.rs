//! RS-CAN-PROJ-017 no_std library without alloc.

#![no_std]

/// Core type re-exported through the no_std crate path.
pub type NoStdRecord = Record;

/// Simple record whose layout is identical under core and std views.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Record {
    pub id: u32,
    pub flag: bool,
}

impl Record {
    pub const fn new(id: u32, flag: bool) -> Self {
        Self { id, flag }
    }
}

/// Label identifying the allocator contract for this crate.
pub fn allocator_label() -> &'static str {
    "no_std:core_only"
}

/// Identical core type construction via the core path.
/// Demonstrates that `core::option::Option` and `std::option::Option` are the
/// same type when `std` is available.
pub fn core_option_example() -> core::option::Option<Record> {
    Some(Record::new(1, true))
}

/// No-std helper that does not depend on `alloc` or `std`.
pub fn checksum(record: &Record) -> u32 {
    record.id.wrapping_add(record.flag as u32)
}
