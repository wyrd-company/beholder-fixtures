//! RS-CAN-TEST-003: documentation test variants and crate-level inclusion.
//!
//! Each function documents one doctest variant. The README inclusion at the
//! crate root provides crate-level documentation inclusion coverage.

// REMOVED explicit include here to avoid duplicating README inclusion already at crate root.
// Use this module to host doctest examples.

/// Runnable variant: compiled and executed by `cargo test --doc`.
///
/// ```
/// assert_eq!(tests_and_documentation::public_api::public_function(), 42);
/// ```
pub fn runnable_demo() -> u32 {
    crate::public_api::public_function()
}

/// No-run variant: compiled but not executed.
///
/// ```no_run
/// let value = tests_and_documentation::public_api::public_function();
/// assert_eq!(value, 42);
/// // This block is type-checked but never run.
/// ```
pub fn no_run_demo() -> u32 {
    crate::public_api::public_function()
}

/// Ignored variant: not compiled or run unless `--ignored` is passed to the harness.
///
/// ```ignore
/// // This block is not compiled during normal `cargo test`.
/// let value = unknown_function();
/// let _ = value;
/// ```
pub fn ignored_demo() -> u32 {
    0
}

/// Should-panic variant: passes when the block panics at runtime (valid source, runtime failure).
///
/// ```should_panic
/// panic!("expected panic for doctest");
/// ```
pub fn should_panic_demo() {
    panic!("expected panic for doctest");
}

/// Hidden-line variant: lines starting with `# ` are hidden in rendered docs but compiled.
///
/// ```
/// # fn hidden_helper() -> u32 { 5 }
/// let value = hidden_helper();
/// assert_eq!(value, 5);
/// ```
pub fn hidden_line_demo() -> u32 {
    5
}

/// Hidden-line with `?` tail: the trailing `?` is inside a hidden line pattern.
///
/// ```
/// # fn fallible() -> Result<u32, &'static str> { Ok(5) }
/// # fn hidden_with_question() -> Result<(), &'static str> {
/// let value = fallible()?;
/// assert_eq!(value, 5);
/// # Ok(())
/// # }
/// # hidden_with_question().unwrap();
/// ```
pub fn hidden_question_demo() -> u32 {
    5
}

/// Edition-tagged variant: compiled under the specified edition.
///
/// ```rust,edition2021
/// let x = 1;
/// assert_eq!(x, 1);
/// ```
pub fn edition_demo() -> u32 {
    1
}
