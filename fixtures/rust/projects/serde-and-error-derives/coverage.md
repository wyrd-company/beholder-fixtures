---
relationships:
  references:
    - ground-rules
    - serde-and-error-derives
    - reports/rust/synthesis/checklist
---

# serde-and-error-derives coverage

| Canonical checklist identifier | Stable source path | Named declaration, item, module, crate, attribute, or test | Build context | Additional variant locators |
| --- | --- | --- | --- | --- |
| RS-CAN-ECO-001 | `src/manual_serialization.rs`, `src/serialization_derives.rs`, `docs/counterexamples.md` | Manual `ManualEnvelope` `Serialize`/`Deserialize` impls with external `item_label` rename and conditional `quantity` omission; derived `RenamedRecord` container/field `rename`, `SkippedFields` `skip_serializing`/`skip_deserializing`, `DefaultedRecord` `default`, `TaggedMessage` `tag`/`content` adapter, `FlattenedRecord`/`RecordMetadata` `flatten`, `GenericEnvelope` `bound`; generated `Serialize`/`Deserialize` trait use on derived records | Default `x86_64-unknown-linux-gnu`, edition 2024, stable 1.97.1 with `serde-derive` enabled | Dependency-feature-gated context builds with `--no-default-features`, compiling manual serialization only; `docs/counterexamples.md` and `src/counterexample_docs.rs` document conflicting helpers and missing derive-feature counterexamples |
| RS-CAN-ECO-002 | `src/manual_errors.rs`, `src/error_derives.rs`, `src/conversion_flow.rs`, `docs/counterexamples.md` | Manual `ManualIoLayer`, `ManualAppError`, `ManualServiceError` with hand-written `Display`/`Error`/`source`/`From` and type-erased boundary; derived `IoLayer`, `ParseLayer`, `AppError` `#[from]`/`#[source]`, `ServiceError` source chain; `service_operation` and `apply_pipeline` consume conversions through `?` | Default with `thiserror-std` enabled | `--no-default-features` retains manual/type-erased boundary without `thiserror/std`; counterexamples for duplicate `source`/`from` and missing conversion in `docs/counterexamples.md` |
