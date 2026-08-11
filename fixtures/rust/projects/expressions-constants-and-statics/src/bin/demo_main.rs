//! Binary demonstrating `main -> Result` with `?` propagation.

use std::fmt;

#[derive(Debug)]
pub struct HarvestError(pub String);

impl fmt::Display for HarvestError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "harvest error: {}", self.0)
    }
}

impl std::error::Error for HarvestError {}

fn may_fail(fail: bool) -> Result<i32, HarvestError> {
    if fail {
        Err(HarvestError("failure".to_string()))
    } else {
        Ok(5)
    }
}

fn main() -> Result<(), HarvestError> {
    let value = may_fail(false)?;
    let _ = value + 10;
    Ok(())
}
