//! RS-CAN-PROJ-017 alloc-using no_std variant.

#![no_std]

extern crate alloc;

use alloc::string::{String, ToString};
use alloc::vec::Vec;

/// Re-exported record identical to the no_std crate's `Record`.
pub use ffi_no_std::Record;

/// Build a heap-allocated description using `alloc`.
pub fn alloc_record_label(record: &Record) -> String {
    let mut out = String::from("record:");
    out.push_str(&record.id.to_string());
    out
}

/// Collect records into a `Vec` via `alloc`.
pub fn alloc_vec_example(ids: &[u32]) -> Vec<Record> {
    ids.iter().map(|&id| Record::new(id, id % 2 == 0)).collect()
}

/// Accessor that proves the same `Record` type flows through `core`,
/// `alloc`, and (when present) `std` paths.
pub fn record_from_alloc(vec: &[Record], index: usize) -> Option<Record> {
    vec.get(index).copied()
}

/// Alloc-specific checksum that still delegates to the core implementation.
pub fn alloc_checksum(records: &[Record]) -> u32 {
    records
        .iter()
        .fold(0, |acc, r| acc.wrapping_add(ffi_no_std::checksum(r)))
}
