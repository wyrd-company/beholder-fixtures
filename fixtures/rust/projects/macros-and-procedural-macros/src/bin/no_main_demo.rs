#![no_main]
#![allow(unused)]

//! RS-CAN-PROJ-018: no_main demonstration.
//! `\#![no_main]` suppresses the `main` requirement. A `\#\[unsafe(no_mangle)]`
//! shim preserves linkage for the default host target.

#[unsafe(no_mangle)]
fn main() {}

// Counterexample: binary without `#![no_main]` and without `fn main` would fail with
// `error: `main` function not found in crate`.
