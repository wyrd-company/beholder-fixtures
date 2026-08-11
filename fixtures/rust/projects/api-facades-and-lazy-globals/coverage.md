---
relationships:
  references:
    - ground-rules
    - api-facades-and-lazy-globals
    - reports/rust/synthesis/checklist
---

# api-facades-and-lazy-globals coverage

| Canonical checklist identifier | Stable source path | Named declaration, item, module, crate, attribute, or test | Build context | Additional variant locators |
| --- | --- | --- | --- | --- |
| RS-CAN-ECO-005 | `src/prelude.rs`, `src/extension.rs`, `src/sealed.rs`, `src/wrappers.rs`, `src/facade.rs`, `src/core.rs`, `crates/facade_downstream/src/lib.rs` | Prelude glob `prelude` module with `pub use` re-exports and `PRELUDE_GLOB`; blanket `CatalogExt` for `T: CatalogEntry`; sealed `CatalogEntry` with private `Sealed` supertrait; `RecordId` newtype and `RecordView` `Deref` wrapper; facade re-exports of `Token`, `CatalogItem`, `RecordId`, `RecordView` consumed via `facade::` and `core::` paths | Default; cross-crate via `facade_downstream` | `docs/counterexamples.md` preserves downstream sealed-impl failure, extension ambiguity, and partial-facade counterexamples |
| RS-CAN-ECO-006 | `src/lazy_globals.rs`, `vendor/lazy_static/` | `OnceLock` `SHARED_CONFIG`, `LazyLock` `SHARED_REGISTRY`, legacy `lazy_static!` `LEGACY_COUNTER` with ordinary `load`/`fetch_add` syntax through hidden wrapper | Default | `docs/counterexamples.md` documents reentrancy/panic counterexample; vendored `lazy_static` 1.5.0 at `vendor/lazy_static/` with `LICENSE-MIT`, `LICENSE-APACHE`, `.cargo-checksum.json`, and `.cargo/config.toml` offline replacement |
| RS-CAN-ECO-010 | `src/naming.rs` | No-`get_` accessors `Metric::value`, `Label::text`; `as_` conversions `as_ratio`, `as_str`; `to_` conversions `to_basis_points`, `to_owned_string`; `into_` conversions `into_parts`, `into_inner`; standard traits `Debug`, `Clone`, `Default`, `PartialEq`, `Eq`, `Hash` on `Label` and `Metric` | Default | `docs/counterexamples.md` documents valid non-conforming `get_value` API counterexample |

## Vendoring provenance

| Crate | Version | Source location | License / notices | Checksum |
| --- | --- | --- | --- | --- |
| `lazy_static` | 1.5.0 | `vendor/lazy_static/` | `vendor/lazy_static/LICENSE-MIT`, `vendor/lazy_static/LICENSE-APACHE` | `bbd2bcb4c963f2ddae06a2efc7e9f3591312473c50c6685e1f298068316e66fe` (from `Cargo.lock`) |

## Decisions

- Used a catalog/token domain theme with generic naming per ground rules.
- Sealed trait uses private-module supertrait pattern rather than private-signature sealing.
- Downstream crate `facade_downstream` is a workspace member built separately in `Taskfile.yml`.
- `lazy_static` 1.5.0 vendored locally; not shared with sibling projects.
