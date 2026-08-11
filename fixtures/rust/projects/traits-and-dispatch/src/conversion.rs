//! RS-CAN-TRAIT-011 — explicit conversion traits.

use std::num::ParseIntError;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UserId(pub u32);

impl From<u32> for UserId {
    fn from(value: u32) -> Self {
        Self(value)
    }
}

#[derive(Debug, Clone)]
pub struct CheckedId(pub u32);

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ConversionError(pub String);

impl std::fmt::Display for ConversionError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl std::error::Error for ConversionError {}

impl TryFrom<i64> for CheckedId {
    type Error = ConversionError;
    fn try_from(value: i64) -> Result<Self, Self::Error> {
        if value < 0 || value > u32::MAX as i64 {
            Err(ConversionError(format!("out of range: {value}")))
        } else {
            Ok(Self(value as u32))
        }
    }
}

impl TryFrom<String> for CheckedId {
    type Error = ParseIntError;
    fn try_from(value: String) -> Result<Self, Self::Error> {
        let parsed: i64 = value.parse()?;
        Ok(Self(parsed as u32))
    }
}

/// Demonstrates reciprocal blanket Into: every From implies Into.
pub fn accepts_into<T: Into<UserId>>(input: T) -> UserId {
    input.into()
}

/// Generic bound driven by conversion trait.
pub fn convert_checked<T>(value: T) -> Result<CheckedId, ConversionError>
where
    CheckedId: TryFrom<T, Error = ConversionError>,
{
    CheckedId::try_from(value)
}

/// `?` error conversion via From: ParseIntError converts through propagated function.
pub fn parse_and_validate(input: &str) -> Result<CheckedId, ConversionError> {
    let parsed: i64 = input
        .parse()
        .map_err(|e: ParseIntError| ConversionError(e.to_string()))?;
    CheckedId::try_from(parsed)
}

/// Additional `?` demonstration with TryFrom and From error conversion.
pub fn try_from_with_question(value: i64) -> Result<CheckedId, ConversionError> {
    let id = CheckedId::try_from(value)?;
    Ok(id)
}

pub fn conversion_summary() -> String {
    let a: UserId = UserId::from(10_u32);
    let b: UserId = 20_u32.into();
    let c = accepts_into(30_u32);
    let d = CheckedId::try_from(42_i64).unwrap();
    let e = try_from_with_question(5).unwrap();
    let f = parse_and_validate("7").unwrap();
    // Invalid implicit conversion counterexample is preserved in docs:
    // `let _id: UserId = 10_u32;` is rejected — explicit From/Into required.
    format!("{a:?}|{b:?}|{c:?}|{d:?}|{e:?}|{f:?}")
}
