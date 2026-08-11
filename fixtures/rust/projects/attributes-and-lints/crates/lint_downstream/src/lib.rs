//! Cross-crate boundary for non-exhaustive and lint-cap demonstrations.

/// Non-exhaustive enum consumed from the parent fixture crate.
#[non_exhaustive]
pub enum ExternalChoice {
    /// First variant.
    Alpha,
    /// Second variant.
    Beta,
}

/// Non-exhaustive struct for update-pattern coverage.
#[non_exhaustive]
pub struct ExternalRecord {
    /// Public field.
    pub value: i32,
}

/// Constructor for cross-crate non-exhaustive struct construction.
pub fn external_record(value: i32) -> ExternalRecord {
    ExternalRecord { value }
}

/// Deprecated cross-crate item.
#[deprecated(note = "prefer ExternalRecord::value")]
pub fn legacy_reader(record: &ExternalRecord) -> i32 {
    record.value
}

/// Must-use return from the downstream crate.
#[must_use = "record the downstream score"]
pub fn downstream_score() -> i32 {
    7
}
