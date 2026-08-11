//! API naming families and standard-trait conventions.

use std::hash::{Hash, Hasher};

/// Metric value demonstrating no-`get_` accessors and conversion naming.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Metric {
    value: f64,
}

impl Metric {
    /// Construct a metric from a scalar value.
    pub const fn new(value: f64) -> Self {
        Self { value }
    }

    /// Borrowed scalar accessor without a `get_` prefix.
    pub const fn value(self) -> f64 {
        self.value
    }

    /// `as_` conversion returning a borrowed view of the same representation.
    pub const fn as_ratio(self) -> f64 {
        self.value
    }

    /// `to_` conversion producing an owned transformed value.
    pub fn to_basis_points(self) -> i64 {
        (self.value * 10_000.0).round() as i64
    }

    /// `into_` conversion consuming `self` and returning owned parts.
    pub fn into_parts(self) -> (i64, i64) {
        let whole = self.value.trunc() as i64;
        let fraction = ((self.value.fract()) * 1_000.0).round() as i64;
        (whole, fraction)
    }
}

impl Default for Metric {
    fn default() -> Self {
        Self::new(0.0)
    }
}

/// Label newtype with standard trait implementations.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct Label(pub String);

impl Label {
    /// Construct a label from owned text.
    pub fn new(text: impl Into<String>) -> Self {
        Self(text.into())
    }

    /// Borrowed text accessor without a `get_` prefix.
    pub fn text(&self) -> &str {
        &self.0
    }

    /// `as_` conversion to a string slice.
    pub fn as_str(&self) -> &str {
        &self.0
    }

    /// `to_` conversion cloning the owned backing string.
    pub fn to_owned_string(&self) -> String {
        self.0.clone()
    }

    /// `into_` conversion consuming the label.
    pub fn into_inner(self) -> String {
        self.0
    }
}

impl Hash for Label {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.0.hash(state);
    }
}

/// Summarize naming conventions exercised in this module.
pub fn naming_summary(metric: Metric, label: &Label) -> String {
    let basis_points = metric.to_basis_points();
    let (whole, fraction) = metric.into_parts();
    format!(
        "label={}:basis_points={}:parts={}:{}",
        label.as_str(),
        basis_points,
        whole,
        fraction
    )
}
