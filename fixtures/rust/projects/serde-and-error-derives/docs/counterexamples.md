# Counterexamples (documentation only)

These named failure modes are preserved beside the valid demonstrations in
`serde-and-error-derives`. They are not compiled as invalid corpus source.

## RS-CAN-ECO-001 — serialization derives

| Counterexample | Why it is invalid |
| --- | --- |
| Conflicting rename helpers | Two `rename` attributes on one item disagree about the external name. |
| Incompatible `remote` / `with` adapters | Adapter attributes reference shapes that cannot be reconciled. |
| Missing derive feature gate | `#[derive(Serialize, Deserialize)]` without enabling `serde/derive` fails at compile time. |

Generated external names such as `displayName`, `renamed_record`, and `meta_version`
are documentation-level wire identifiers, not Rust identifiers in the fixture source.

## RS-CAN-ECO-002 — error derives

| Counterexample | Why it is invalid |
| --- | --- |
| Duplicate `#[source]` fields | More than one source field is rejected by the derive crate. |
| Duplicate `#[from]` fields | Two `from` fields for the same conversion edge are rejected. |
| Missing conversion edge | Using `?` without a generated `From` impl fails type checking. |
