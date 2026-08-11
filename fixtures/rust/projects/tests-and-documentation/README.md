# tests-and-documentation

Fixture crate demonstrating Rust test and documentation compilation model.

This README is included as crate-level documentation via
`#![doc = include_str!("../README.md")]` in `src/lib.rs`.

Example from crate docs:

```rust
let value = tests_and_documentation::public_api::public_function();
assert_eq!(value, 42);
```
