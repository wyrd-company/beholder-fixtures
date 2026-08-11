//! Documentation-only counterexamples preserved beside valid demonstrations.

/// Named counterexamples for serialization derives (documentation only).
///
/// Invalid patterns that must not appear as corpus source:
/// - Conflicting helpers such as `#[serde(rename = "a")]` combined with
///   `#[serde(rename = "b")]` on the same item.
/// - `remote` and `with` adapters pointing at incompatible external shapes.
/// - Generated external names such as `displayName` that are not Rust identifiers.
pub struct SerializationCounterexamples;

/// Named counterexamples for error derives (documentation only).
///
/// Invalid patterns that must not appear as corpus source:
/// - Duplicate `#[source]` fields on one error variant.
/// - Duplicate `#[from]` fields selecting the same conversion edge twice.
/// - Missing `From` conversion when `?` expects a typed edge.
pub struct ErrorCounterexamples;

/// Summary anchor for counterexample documentation.
pub fn counterexample_summary() -> &'static str {
    let _ = (SerializationCounterexamples, ErrorCounterexamples);
    "counterexample_docs"
}
