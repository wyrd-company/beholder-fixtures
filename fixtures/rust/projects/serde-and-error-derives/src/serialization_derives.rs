//! Derive-generated serialization helpers: rename, skip, default, flatten/tag adapters,
//! generic bounds, and generated trait use.

use serde::{Deserialize, Serialize};

/// Container rename maps the Rust struct to the external name `renamed_record`.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename = "renamed_record")]
pub struct RenamedRecord {
    /// Field rename maps `display_name` to `displayName` on the wire.
    #[serde(rename = "displayName")]
    pub display_name: String,
    /// Internal counter kept under the Rust field name.
    pub revision: u32,
}

/// Skip helpers omit selected fields from one direction of the wire format.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SkippedFields {
    pub visible: String,
    #[serde(skip_serializing)]
    pub cache_only: String,
    #[serde(skip_deserializing)]
    pub export_only: String,
}

/// Default helper supplies missing wire fields during deserialization.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DefaultedRecord {
    pub title: String,
    #[serde(default)]
    pub priority: u8,
    #[serde(default = "default_channel")]
    pub channel: String,
}

fn default_channel() -> String {
    "general".to_owned()
}

/// Tag adapter encodes enum variants with an external discriminator field.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", content = "payload")]
pub enum TaggedMessage {
    /// Variant rename maps `Ping` to `ping` on the wire.
    #[serde(rename = "ping")]
    Ping {
        #[serde(rename = "seq")]
        sequence: u32,
    },
    Notice {
        text: String,
    },
}

/// Flatten adapter inlines a nested record into the parent object.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FlattenedRecord {
    pub id: u64,
    #[serde(flatten)]
    pub metadata: RecordMetadata,
}

/// Nested metadata flattened into the parent wire object.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct RecordMetadata {
    #[serde(rename = "meta_version")]
    pub version: u32,
    pub owner: String,
}

/// Generic bounds constrain generated trait impls for type parameters.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(bound(serialize = "T: Serialize", deserialize = "T: Deserialize<'de>"))]
pub struct GenericEnvelope<T> {
    pub label: String,
    pub value: T,
}

/// Summary anchor for derive-generated serialization coverage.
pub fn derived_serialization_summary() -> &'static str {
    "serialization_derives"
}
