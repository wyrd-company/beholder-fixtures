//! Conversion flow tying serialization and error demonstrations together.

use crate::error_derives::{AppError, IoLayer, ParseLayer, ServiceError, service_operation};
use crate::manual_errors::{ManualAppError, ManualIoLayer, ManualServiceError};

/// Applies both manual and derived conversion pipelines for fixture linkage.
pub fn apply_pipeline(label: &str) -> (Result<u32, ManualServiceError>, Result<u32, ServiceError>) {
    let manual = ManualIoLayer::new(label);
    let manual_app: ManualAppError = manual.into();
    let manual_result = Err(ManualServiceError::erase("pipeline manual", manual_app));

    let derived = service_operation(label, "token");
    (manual_result, derived)
}

/// Summary anchor for cross-module conversion flow.
pub fn pipeline_summary() -> &'static str {
    "conversion_flow"
}

/// Retains derived error types for dead-code analysis across feature sets.
#[allow(dead_code)]
fn retain_derived_types() {
    let _ = AppError::Io(IoLayer {
        path: "anchor".to_owned(),
    });
    let _ = AppError::Parse(ParseLayer {
        token: "anchor".to_owned(),
        cause: IoLayer {
            path: "anchor".to_owned(),
        },
    });
}
