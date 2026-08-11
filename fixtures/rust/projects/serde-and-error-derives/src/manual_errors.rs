//! Manual `Display`, `Error`, `source`, and `From` implementations contrasting
//! derive-generated conversion edges.

use core::error::Error;
use core::fmt::{self, Display};

/// Leaf failure with a stable manual display message.
#[derive(Debug)]
pub struct ManualIoLayer {
    detail: String,
}

impl ManualIoLayer {
    /// Constructs a leaf manual error.
    pub fn new(detail: impl Into<String>) -> Self {
        Self {
            detail: detail.into(),
        }
    }
}

impl Display for ManualIoLayer {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "manual io failure: {}", self.detail)
    }
}

impl Error for ManualIoLayer {}

/// Application boundary error composed from a manual leaf and a manual conversion.
#[derive(Debug)]
pub struct ManualAppError {
    context: String,
    source: ManualIoLayer,
}

impl ManualAppError {
    /// Wraps a leaf failure with additional context.
    pub fn wrap(context: impl Into<String>, source: ManualIoLayer) -> Self {
        Self {
            context: context.into(),
            source,
        }
    }
}

impl Display for ManualAppError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}: {}", self.context, self.source)
    }
}

impl Error for ManualAppError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        Some(&self.source)
    }
}

impl From<ManualIoLayer> for ManualAppError {
    fn from(source: ManualIoLayer) -> Self {
        Self::wrap("manual conversion", source)
    }
}

/// Type-erased boundary that accepts any error source through `?`.
#[derive(Debug)]
pub struct ManualServiceError {
    message: String,
    source: Option<Box<dyn Error + Send + Sync>>,
}

impl ManualServiceError {
    /// Erases a concrete error into the service boundary.
    pub fn erase<E>(message: impl Into<String>, source: E) -> Self
    where
        E: Error + Send + Sync + 'static,
    {
        Self {
            message: message.into(),
            source: Some(Box::new(source)),
        }
    }
}

impl Display for ManualServiceError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{}", self.message)
    }
}

impl Error for ManualServiceError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        self.source.as_deref().map(|err| err as &dyn Error)
    }
}

/// Demonstrates manual conversion flow through `?` into the type-erased boundary.
pub fn manual_error_summary() -> Result<u32, ManualServiceError> {
    let leaf = ManualIoLayer::new("missing segment");
    let app: ManualAppError = leaf.into();
    Err(ManualServiceError::erase("manual service boundary", app))
}
