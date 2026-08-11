//! Newtype and `Deref` wrappers controlling field exposure.

use std::ops::Deref;

use crate::core::Token;

/// Opaque record identifier newtype.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct RecordId(u64);

impl RecordId {
    /// Construct a record identifier.
    pub const fn new(value: u64) -> Self {
        Self(value)
    }

    /// Expose the raw identifier without a `get_` prefix.
    pub const fn raw(self) -> u64 {
        self.0
    }
}

/// Borrowed view over a record identifier via `Deref`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct RecordView {
    id: RecordId,
    token: Token,
}

impl RecordView {
    /// Build a view from an identifier and token.
    pub const fn new(id: RecordId, token: Token) -> Self {
        Self { id, token }
    }

    /// Access the wrapped token directly.
    pub const fn token(self) -> Token {
        self.token
    }
}

impl Deref for RecordView {
    type Target = RecordId;

    fn deref(&self) -> &Self::Target {
        &self.id
    }
}

/// Combine wrapper identities into a stable summary string.
pub fn wrapper_summary(view: &RecordView) -> String {
    format!("record:{}:token:{}", view.raw(), view.token().value())
}
