//! Manual `Serialize` and `Deserialize` implementations contrasting derive-generated
//! helpers whose external names, bounds, and defaults differ from Rust identifiers.

use core::fmt;

/// External wire name `manual_envelope` differs from the Rust identifier.
pub struct ManualEnvelope {
    /// Serialized as `item_label` rather than `label`.
    pub label: String,
    /// Omitted on the wire when equal to the default `0`.
    pub quantity: u32,
}

impl ManualEnvelope {
    /// Stable label for coverage locators.
    pub const LABEL: &'static str = "manual_envelope";
}

impl serde::Serialize for ManualEnvelope {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        use serde::ser::SerializeStruct;
        let mut state = serializer.serialize_struct(Self::LABEL, 2)?;
        state.serialize_field("item_label", &self.label)?;
        if self.quantity != 0 {
            state.serialize_field("quantity", &self.quantity)?;
        }
        state.end()
    }
}

impl<'de> serde::Deserialize<'de> for ManualEnvelope {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: serde::Deserializer<'de>,
    {
        use serde::de::{self, MapAccess, Visitor};
        struct EnvelopeVisitor;

        impl<'de> Visitor<'de> for EnvelopeVisitor {
            type Value = ManualEnvelope;

            fn expecting(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
                formatter.write_str("a map with item_label and optional quantity")
            }

            fn visit_map<A>(self, mut map: A) -> Result<Self::Value, A::Error>
            where
                A: MapAccess<'de>,
            {
                let mut label = None;
                let mut quantity = 0;
                while let Some(key) = map.next_key::<String>()? {
                    match key.as_str() {
                        "item_label" => {
                            if label.is_some() {
                                return Err(de::Error::duplicate_field("item_label"));
                            }
                            label = Some(map.next_value()?);
                        }
                        "quantity" => quantity = map.next_value()?,
                        other => {
                            return Err(de::Error::unknown_field(
                                other,
                                &["item_label", "quantity"],
                            ));
                        }
                    }
                }
                let label = label.ok_or_else(|| de::Error::missing_field("item_label"))?;
                Ok(ManualEnvelope { label, quantity })
            }
        }

        deserializer.deserialize_map(EnvelopeVisitor)
    }
}

/// Summary anchor for manual serialization coverage.
pub fn manual_serialization_summary() -> &'static str {
    "manual_serialization"
}
