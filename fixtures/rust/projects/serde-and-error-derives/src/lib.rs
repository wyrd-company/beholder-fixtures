//! Fixture demonstrating serialization-style and error-derive ecosystem conventions.

#![warn(missing_docs)]
// Derive-generated items are not fixture-authored documentation.
#![allow(missing_docs)]

mod conversion_flow;
mod counterexample_docs;
mod error_derives;
mod manual_errors;
mod manual_serialization;
#[cfg(feature = "serde-derive")]
mod serialization_derives;

pub use conversion_flow::{apply_pipeline, pipeline_summary};
pub use counterexample_docs::counterexample_summary;
pub use error_derives::{
    AppError, IoLayer, ParseLayer, ServiceError, derived_error_summary, service_operation,
};
pub use manual_errors::{ManualAppError, ManualServiceError, manual_error_summary};
pub use manual_serialization::{ManualEnvelope, manual_serialization_summary};
#[cfg(feature = "serde-derive")]
pub use serialization_derives::{
    DefaultedRecord, FlattenedRecord, GenericEnvelope, RenamedRecord, SkippedFields, TaggedMessage,
    derived_serialization_summary,
};

/// Project-level summary tying serialization and error modules together.
pub fn fixture_summary() -> &'static str {
    "serde-and-error-derives"
}
