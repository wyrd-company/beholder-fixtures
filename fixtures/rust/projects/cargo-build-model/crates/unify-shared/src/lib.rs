//! RS-CAN-PROJ-007: feature unification under resolver versions 1,2,3.
#[cfg(all(feature = "feat-a", not(feature = "feat-b")))]
pub fn active_features() -> &'static str {
    "feat-a"
}
#[cfg(all(feature = "feat-b", not(feature = "feat-a")))]
pub fn active_features() -> &'static str {
    "feat-b"
}
#[cfg(all(feature = "feat-a", feature = "feat-b"))]
pub fn active_features() -> &'static str {
    "feat-a+feat-b"
}
#[cfg(not(any(feature = "feat-a", feature = "feat-b")))]
pub fn active_features() -> &'static str {
    "none"
}

pub fn version() -> &'static str {
    "0.1.0"
}
