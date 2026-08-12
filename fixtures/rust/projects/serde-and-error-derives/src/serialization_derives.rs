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

/// Invokes the derive-generated `Serialize` and `Deserialize` impls on `RenamedRecord`.
pub fn invoke_renamed_record_serde(record: RenamedRecord) -> RenamedRecord {
    wire::invoke_renamed_record_serde(record)
}

/// Summary anchor for derive-generated serialization coverage.
pub fn derived_serialization_summary() -> &'static str {
    let _ = invoke_renamed_record_serde(RenamedRecord {
        display_name: "fixture".to_owned(),
        revision: 1,
    });
    "serialization_derives"
}

mod wire {
    use core::fmt;
    use core::marker::PhantomData;

    use serde::de::{self, Deserializer, MapAccess, Visitor};
    use serde::ser::{Serialize, SerializeStruct, Serializer};

    type WireFields = Vec<(String, String)>;

    #[derive(Debug)]
    struct WireSerError(String);

    impl fmt::Display for WireSerError {
        fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
            formatter.write_str(&self.0)
        }
    }

    impl serde::ser::Error for WireSerError {
        fn custom<T: fmt::Display>(msg: T) -> Self {
            Self(msg.to_string())
        }
    }

    #[derive(Debug)]
    struct WireDeError(String);

    impl fmt::Display for WireDeError {
        fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
            formatter.write_str(&self.0)
        }
    }

    impl de::Error for WireDeError {
        fn custom<T: fmt::Display>(msg: T) -> Self {
            Self(msg.to_string())
        }
    }

    struct WireSerializer;

    struct StructSerializer {
        fields: WireFields,
    }

    #[derive(Default)]
    struct ScalarSerializer;

    impl Serializer for WireSerializer {
        type Ok = WireFields;
        type Error = WireSerError;
        type SerializeSeq = serde::ser::Impossible<Self::Ok, Self::Error>;
        type SerializeTuple = serde::ser::Impossible<Self::Ok, Self::Error>;
        type SerializeTupleStruct = serde::ser::Impossible<Self::Ok, Self::Error>;
        type SerializeTupleVariant = serde::ser::Impossible<Self::Ok, Self::Error>;
        type SerializeMap = serde::ser::Impossible<Self::Ok, Self::Error>;
        type SerializeStruct = StructSerializer;
        type SerializeStructVariant = serde::ser::Impossible<Self::Ok, Self::Error>;

        fn serialize_bool(self, _v: bool) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_i8(self, _v: i8) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_i16(self, _v: i16) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_i32(self, _v: i32) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_i64(self, _v: i64) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_u8(self, _v: u8) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_u16(self, _v: u16) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_u32(self, _v: u32) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_u64(self, _v: u64) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_f32(self, _v: f32) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_f64(self, _v: f64) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_char(self, _v: char) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_str(self, _v: &str) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_bytes(self, _v: &[u8]) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_none(self) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_some<T>(self, _value: &T) -> Result<Self::Ok, Self::Error>
        where
            T: ?Sized + Serialize,
        {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_unit(self) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_unit_struct(self, _name: &'static str) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_unit_variant(
            self,
            _name: &'static str,
            _variant_index: u32,
            _variant: &'static str,
        ) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_newtype_struct<T>(
            self,
            _name: &'static str,
            _value: &T,
        ) -> Result<Self::Ok, Self::Error>
        where
            T: ?Sized + Serialize,
        {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_newtype_variant<T>(
            self,
            _name: &'static str,
            _variant_index: u32,
            _variant: &'static str,
            _value: &T,
        ) -> Result<Self::Ok, Self::Error>
        where
            T: ?Sized + Serialize,
        {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_seq(self, _len: Option<usize>) -> Result<Self::SerializeSeq, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_tuple(self, _len: usize) -> Result<Self::SerializeTuple, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_tuple_struct(
            self,
            _name: &'static str,
            _len: usize,
        ) -> Result<Self::SerializeTupleStruct, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_tuple_variant(
            self,
            _name: &'static str,
            _variant_index: u32,
            _variant: &'static str,
            _len: usize,
        ) -> Result<Self::SerializeTupleVariant, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_map(self, _len: Option<usize>) -> Result<Self::SerializeMap, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }

        fn serialize_struct(
            self,
            _name: &'static str,
            _len: usize,
        ) -> Result<Self::SerializeStruct, Self::Error> {
            Ok(StructSerializer { fields: Vec::new() })
        }

        fn serialize_struct_variant(
            self,
            _name: &'static str,
            _variant_index: u32,
            _variant: &'static str,
            _len: usize,
        ) -> Result<Self::SerializeStructVariant, Self::Error> {
            Err(WireSerError("unsupported wire type".to_owned()))
        }
    }

    impl SerializeStruct for StructSerializer {
        type Ok = WireFields;
        type Error = WireSerError;

        fn serialize_field<T>(&mut self, key: &'static str, value: &T) -> Result<(), Self::Error>
        where
            T: ?Sized + Serialize,
        {
            let scalar = value.serialize(ScalarSerializer)?;
            self.fields.push((key.to_owned(), scalar));
            Ok(())
        }

        fn end(self) -> Result<Self::Ok, Self::Error> {
            Ok(self.fields)
        }
    }

    impl Serializer for ScalarSerializer {
        type Ok = String;
        type Error = WireSerError;
        type SerializeSeq = serde::ser::Impossible<Self::Ok, Self::Error>;
        type SerializeTuple = serde::ser::Impossible<Self::Ok, Self::Error>;
        type SerializeTupleStruct = serde::ser::Impossible<Self::Ok, Self::Error>;
        type SerializeTupleVariant = serde::ser::Impossible<Self::Ok, Self::Error>;
        type SerializeMap = serde::ser::Impossible<Self::Ok, Self::Error>;
        type SerializeStruct = serde::ser::Impossible<Self::Ok, Self::Error>;
        type SerializeStructVariant = serde::ser::Impossible<Self::Ok, Self::Error>;

        fn serialize_bool(self, _v: bool) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_i8(self, _v: i8) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_i16(self, _v: i16) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_i32(self, _v: i32) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_i64(self, _v: i64) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_u8(self, v: u8) -> Result<Self::Ok, Self::Error> {
            self.serialize_u32(u32::from(v))
        }

        fn serialize_u16(self, v: u16) -> Result<Self::Ok, Self::Error> {
            self.serialize_u32(u32::from(v))
        }

        fn serialize_u32(self, v: u32) -> Result<Self::Ok, Self::Error> {
            Ok(v.to_string())
        }

        fn serialize_u64(self, v: u64) -> Result<Self::Ok, Self::Error> {
            Ok(v.to_string())
        }

        fn serialize_f32(self, _v: f32) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_f64(self, _v: f64) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_char(self, _v: char) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_str(self, v: &str) -> Result<Self::Ok, Self::Error> {
            Ok(v.to_owned())
        }

        fn serialize_bytes(self, _v: &[u8]) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_none(self) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_some<T>(self, _value: &T) -> Result<Self::Ok, Self::Error>
        where
            T: ?Sized + Serialize,
        {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_unit(self) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_unit_struct(self, _name: &'static str) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_unit_variant(
            self,
            _name: &'static str,
            _variant_index: u32,
            _variant: &'static str,
        ) -> Result<Self::Ok, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_newtype_struct<T>(
            self,
            _name: &'static str,
            _value: &T,
        ) -> Result<Self::Ok, Self::Error>
        where
            T: ?Sized + Serialize,
        {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_newtype_variant<T>(
            self,
            _name: &'static str,
            _variant_index: u32,
            _variant: &'static str,
            _value: &T,
        ) -> Result<Self::Ok, Self::Error>
        where
            T: ?Sized + Serialize,
        {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_seq(self, _len: Option<usize>) -> Result<Self::SerializeSeq, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_tuple(self, _len: usize) -> Result<Self::SerializeTuple, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_tuple_struct(
            self,
            _name: &'static str,
            _len: usize,
        ) -> Result<Self::SerializeTupleStruct, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_tuple_variant(
            self,
            _name: &'static str,
            _variant_index: u32,
            _variant: &'static str,
            _len: usize,
        ) -> Result<Self::SerializeTupleVariant, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_map(self, _len: Option<usize>) -> Result<Self::SerializeMap, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_struct(
            self,
            _name: &'static str,
            _len: usize,
        ) -> Result<Self::SerializeStruct, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }

        fn serialize_struct_variant(
            self,
            _name: &'static str,
            _variant_index: u32,
            _variant: &'static str,
            _len: usize,
        ) -> Result<Self::SerializeStructVariant, Self::Error> {
            Err(WireSerError("unsupported scalar".to_owned()))
        }
    }

    struct WireDeserializer<'a> {
        fields: &'a [(String, String)],
        index: usize,
        current_key: Option<String>,
    }

    impl<'a> WireDeserializer<'a> {
        fn new(fields: &'a [(String, String)]) -> Self {
            Self {
                fields,
                index: 0,
                current_key: None,
            }
        }
    }

    impl<'de> Deserializer<'de> for WireDeserializer<'de> {
        type Error = WireDeError;

        fn deserialize_any<V>(self, _visitor: V) -> Result<V::Value, Self::Error>
        where
            V: Visitor<'de>,
        {
            Err(WireDeError("unsupported wire type".to_owned()))
        }

        serde::forward_to_deserialize_any! {
            bool i8 i16 i32 i64 u8 u16 u32 u64 f32 f64 char str string bytes
            byte_buf option unit unit_struct newtype_struct seq tuple
            tuple_struct map enum identifier ignored_any
        }

        fn deserialize_struct<V>(
            self,
            _name: &'static str,
            _fields: &'static [&'static str],
            visitor: V,
        ) -> Result<V::Value, Self::Error>
        where
            V: Visitor<'de>,
        {
            visitor.visit_map(self)
        }
    }

    impl<'de> MapAccess<'de> for WireDeserializer<'de> {
        type Error = WireDeError;

        fn next_key_seed<K>(&mut self, seed: K) -> Result<Option<K::Value>, Self::Error>
        where
            K: de::DeserializeSeed<'de>,
        {
            if self.index >= self.fields.len() {
                return Ok(None);
            }
            let key = &self.fields[self.index].0;
            self.current_key = Some(key.clone());
            seed.deserialize(KeyDeserializer {
                key: key.as_str(),
                marker: PhantomData,
            })
            .map(Some)
        }

        fn next_value_seed<V>(&mut self, seed: V) -> Result<V::Value, Self::Error>
        where
            V: de::DeserializeSeed<'de>,
        {
            let key = self
                .current_key
                .take()
                .ok_or_else(|| WireDeError("missing field key".to_owned()))?;
            let value = self
                .fields
                .get(self.index)
                .filter(|(field, _)| field == &key)
                .map(|(_, value)| value.as_str())
                .ok_or_else(|| WireDeError("missing field value".to_owned()))?;
            self.index += 1;
            seed.deserialize(ValueDeserializer {
                value,
                marker: PhantomData,
            })
        }
    }

    struct KeyDeserializer<'de> {
        key: &'de str,
        marker: PhantomData<&'de ()>,
    }

    impl<'de> Deserializer<'de> for KeyDeserializer<'de> {
        type Error = WireDeError;

        fn deserialize_any<V>(self, visitor: V) -> Result<V::Value, Self::Error>
        where
            V: Visitor<'de>,
        {
            visitor.visit_str(self.key)
        }

        serde::forward_to_deserialize_any! {
            bool i8 i16 i32 i64 u8 u16 u32 u64 f32 f64 char str string bytes
            byte_buf option unit unit_struct newtype_struct seq tuple
            tuple_struct map struct enum identifier ignored_any
        }
    }

    struct ValueDeserializer<'de> {
        value: &'de str,
        marker: PhantomData<&'de ()>,
    }

    impl<'de> Deserializer<'de> for ValueDeserializer<'de> {
        type Error = WireDeError;

        fn deserialize_any<V>(self, visitor: V) -> Result<V::Value, Self::Error>
        where
            V: Visitor<'de>,
        {
            visitor.visit_str(self.value)
        }

        serde::forward_to_deserialize_any! {
            bool i8 i16 i32 i64 u8 u16 u64 f32 f64 char str string bytes
            byte_buf option unit unit_struct newtype_struct seq tuple
            tuple_struct map struct enum identifier ignored_any
        }

        fn deserialize_u32<V>(self, visitor: V) -> Result<V::Value, Self::Error>
        where
            V: Visitor<'de>,
        {
            let parsed = self
                .value
                .parse::<u32>()
                .map_err(|_| WireDeError("invalid u32".to_owned()))?;
            visitor.visit_u32(parsed)
        }
    }

    pub(super) fn invoke_renamed_record_serde(
        record: super::RenamedRecord,
    ) -> super::RenamedRecord {
        let wire: Vec<(String, String)> = match serde::Serialize::serialize(&record, WireSerializer)
        {
            Ok(fields) => fields,
            Err(_err) => panic!("serialize derived record"),
        };
        match serde::Deserialize::deserialize(WireDeserializer::new(&wire)) {
            Ok(restored) => restored,
            Err(_err) => panic!("deserialize derived record"),
        }
    }
}
