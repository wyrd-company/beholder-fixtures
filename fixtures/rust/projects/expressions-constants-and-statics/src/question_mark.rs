//! RS-CAN-EXPR-006 — `?`, residuals, and conversions.

use std::fmt;

/// Custom error type demonstrating `From` conversion via `?`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct HarvestError(pub String);

impl fmt::Display for HarvestError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "harvest error: {}", self.0)
    }
}

impl std::error::Error for HarvestError {}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FieldError(pub String);

impl fmt::Display for FieldError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "field error: {}", self.0)
    }
}

impl std::error::Error for FieldError {}

impl From<FieldError> for HarvestError {
    fn from(value: FieldError) -> Self {
        HarvestError(value.0)
    }
}

fn may_fail_field(fail: bool) -> Result<i32, FieldError> {
    if fail {
        Err(FieldError("field failed".to_string()))
    } else {
        Ok(7)
    }
}

/// `?` on `Result` with error conversion through `FromResidual`.
pub fn result_with_conversion(fail: bool) -> Result<i32, HarvestError> {
    let value = may_fail_field(fail)?;
    Ok(value + 10)
}

/// `?` on `Option` with early return.
pub fn option_try(value: Option<i32>) -> Option<i32> {
    let inner = value?;
    Some(inner * 2)
}

/// Nested closure context: `?` inside closure must match closure return type, not outer function.
pub fn nested_closure_try() -> Result<i32, HarvestError> {
    let closure = || -> Result<i32, HarvestError> {
        let v = may_fail_field(false).map_err(HarvestError::from)?;
        Ok(v)
    };
    let res = closure()?;
    Ok(res + 1)
}

/// Async context: `?` inside async fn / async block.
pub async fn async_try(fail: bool) -> Result<i32, HarvestError> {
    let v = may_fail_field(fail)?;
    Ok(v + 100)
}

pub async fn async_block_try(fail: bool) -> Result<i32, HarvestError> {
    let fut = async move { may_fail_field(fail) };
    let value = fut.await?;
    Ok(value + 1)
}

/// Closure inside async: nested closure and async both handle `?`.
pub async fn nested_async_closure_try() -> Result<i32, HarvestError> {
    let inner = || async { may_fail_field(false) };
    let val = inner().await?;
    Ok(val)
}

/// `main -> Result` analog: a function returning `Result` that uses `?` at top-level, mirroring `fn main() -> Result`.
pub fn main_like() -> Result<(), HarvestError> {
    let _ = may_fail_field(false)?;
    let _ = option_try(Some(5));
    Ok(())
}

/// Demonstrates chaining `?` and error conversion is selected from enclosing return type.
pub fn chaining_conversion(a_fail: bool, b_fail: bool) -> Result<i32, HarvestError> {
    let a = may_fail_field(a_fail)?;
    let b = may_fail_field(b_fail)?;
    Ok(a + b)
}

pub fn demonstrate() -> i32 {
    let _ = result_with_conversion(false);
    let _ = result_with_conversion(true).is_err();
    let _ = option_try(Some(3));
    let _ = option_try(None);
    let _ = nested_closure_try().is_ok();
    let _ = main_like().is_ok();
    let _ = chaining_conversion(false, false);
    1
}
