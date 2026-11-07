---
relationships:
  references:
    - ground-rules
    - wasm-bindgen-bridge
    - reports/rust/synthesis/checklist
---

# wasm-bindgen-bridge coverage

| Canonical checklist identifier | Stable source path | Named declaration, item, module, crate, attribute, or test | Build context | Additional variant locators |
| --- | --- | --- | --- | --- |
| RS-CAN-ECO-008 | `src/bridge_exports.rs`, `src/bridge_imports.rs`, `src/ownership.rs`, `src/abi_adaptation.rs`, `src/plain_exports.rs`, `src/wasm_target.rs`, `src/lib.rs` | Exported Rust-to-foreign surface `bridge_exports::{add, greet, concat_strings, create_buffer, optional_greeting, is_even, scale, BridgeCounter::new/increment/value/count/set_count/add_to, BridgeStatus::Idle/Active/Done, status_label}` via `#[wasm_bindgen]`; imported foreign items `bridge_imports::{alert, log, console_log_number, math_random}` via `#[wasm_bindgen] extern "C"` and `imported_surface_label`; ownership/ABI adaptation `ownership::{borrowed_len, owned_echo, bytes_sum, owned_bytes, echo_optional, BridgeValue::new/payload/into_payload, ownership_label}` and `abi_adaptation::{primitive_add/scale/negate, string_abi_len/concat, bytes_abi_sum, optional_abi, result_abi, AbiHolder::new/get/set, abi_label}`; plain contrast `plain_exports::{rust_public_add, c_exported_add, C_EXPORTED_VALUE}`; target-gated bridge `wasm_target::{wasm_only_entry, wasm_section_marker, wasm_target_label, call_import_with_fallback}` with `cfg(target_arch="wasm32")` gating and `wasm32-unknown-unknown` build in `Taskfile.yml`; host proc-macro generator `wasm-bindgen` with no tracked generated source (macro expansion only) | Default `x86_64-unknown-linux-gnu` edition 2024 stable 1.99.1; bridge target `wasm32-unknown-unknown` (installed in rustup stable) exercised by `cargo build --offline --target wasm32-unknown-unknown` | `docs/counterexamples.md` preserves non-installed alternative Wasm ABI/interface generator (`wasm32-wasip1` WASI, `cxx`/`pyo3`/`wit-bindgen`) and companion foreign artifact (`wasm-bindgen-cli` `*_bg.js` / `*_bg.wasm` generation) as documentation-only; generated foreign-binding identifiers (e.g., glue helper names) are documentation-level, not Rust identifiers; `Taskfile.yml:build` is offline/hermetic and does not invoke `wasm-bindgen-cli`/`wasm-pack` |

## Vendoring provenance

| Crate | Version | Source location | License / notices | Checksum |
| --- | --- | --- | --- | --- |
| `wasm-bindgen` | 0.2.100 | `vendor/wasm-bindgen/` | `vendor/wasm-bindgen/LICENSE-MIT`, `vendor/wasm-bindgen/LICENSE-APACHE` | `1edc8929d7499fc4e8f0be2262a241556cfc54a0bea223790e71446f2aab1ef5` (from `Cargo.lock`) |
| `wasm-bindgen-macro` | 0.2.100 | `vendor/wasm-bindgen-macro/` | `vendor/wasm-bindgen-macro/LICENSE-MIT`, `vendor/wasm-bindgen-macro/LICENSE-APACHE` | `7fe63fc6d09ed3792bd0897b314f53de8e16568c2b3f7982f468c0bf9bd0b407` |
| `wasm-bindgen-macro-support` | 0.2.100 | `vendor/wasm-bindgen-macro-support/` | `vendor/wasm-bindgen-macro-support/LICENSE-MIT`, `vendor/wasm-bindgen-macro-support/LICENSE-APACHE` | `8ae87ea40c9f689fc23f209965b6fb8a99ad69aeeb0231408be24920604395de` |
| `wasm-bindgen-backend` | 0.2.100 | `vendor/wasm-bindgen-backend/` | `vendor/wasm-bindgen-backend/LICENSE-MIT`, `vendor/wasm-bindgen-backend/LICENSE-APACHE` | `2f0a0651a5c2bc21487bde11ee802ccaf4c51935d0d3d42a6101f98161700bc6` |
| `wasm-bindgen-shared` | 0.2.100 | `vendor/wasm-bindgen-shared/` | `vendor/wasm-bindgen-shared/LICENSE-MIT`, `vendor/wasm-bindgen-shared/LICENSE-APACHE` | `1a05d73b933a847d6cccdda8f838a22ff101ad9bf93e33684f39c1f5f0eece3d` |
| `bumpalo` | 3.20.3 | `vendor/bumpalo/` | `vendor/bumpalo/LICENSE-MIT`, `vendor/bumpalo/LICENSE-APACHE` | `72f5acc6cb2ba439de613abc23857ec3d78374d8ed5ac84e9d11336e87da8649` |
| `cfg-if` | 1.0.4 | `vendor/cfg-if/` | `vendor/cfg-if/LICENSE-MIT`, `vendor/cfg-if/LICENSE-APACHE` | `9330f8b2ff13f34540b44e946ef35111825727b38d33286ef986142615121801` |
| `log` | 0.4.33 | `vendor/log/` | `vendor/log/LICENSE-MIT`, `vendor/log/LICENSE-APACHE` | `0ceec5bc11778974d1bcb055b18002eba7f4b3518b6a0081b3af5f21666da9ad` |
| `once_cell` | 1.21.4 | `vendor/once_cell/` | `vendor/once_cell/LICENSE-MIT`, `vendor/once_cell/LICENSE-APACHE` | `9f7c3e4beb33f85d45ae3e3a1792185706c8e16d043238c593331cc7cd313b50` |
| `proc-macro2` | 1.0.107 | `vendor/proc-macro2/` | `vendor/proc-macro2/LICENSE-MIT`, `vendor/proc-macro2/LICENSE-APACHE` | `985e7ec9bb745e6ce6535b544d84d6cd6f7ad8bd711c398938ae983b91a766d9` |
| `quote` | 1.0.47 | `vendor/quote/` | `vendor/quote/LICENSE-MIT`, `vendor/quote/LICENSE-APACHE` | `1fbf4db142a473a8d80c26bbf18454ed458bf8d26c8219c331daecfdbd079001` |
| `rustversion` | 1.0.23 | `vendor/rustversion/` | `vendor/rustversion/LICENSE-MIT`, `vendor/rustversion/LICENSE-APACHE` | `cf54715a573b99ac80df0bc206da022bcd442c974952c7b9720069370852e21f` |
| `syn` | 2.0.119 | `vendor/syn/` | `vendor/syn/LICENSE-MIT`, `vendor/syn/LICENSE-APACHE` | `872831b642d1a07999a962a351ed35b955ea2cfc8f3862091e2a240a84f17297` |
| `unicode-ident` | 1.0.24 | `vendor/unicode-ident/` | `vendor/unicode-ident/LICENSE-MIT`, `vendor/unicode-ident/LICENSE-APACHE` | `e6e4313cd5fcd3dad5cafa179702e2b244f760991f45397d14d4ebf38247da75` |

All crates vendored under `vendor/` with `.cargo-checksum.json` and `Cargo.toml.orig`; offline builds use `.cargo/config.toml` `replace-with = "vendored-sources"` (source `https://crates.io/crates/<crate>/<version>` for each).

## Decisions

- Theme uses generic bridge/counter/payload domain per ground rules.
- `crate-type = ["cdylib", "rlib"]` so the crate produces wasm link output on `wasm32-unknown-unknown` while remaining usable as `rlib` on host.
- Target gating uses `#[cfg(target_arch = "wasm32")]` on `wasm_target` items; `wasm-bindgen` attributes themselves are present on both targets and expand via host proc-macro.
- Downstream JS-binding CLI (`wasm-bindgen-cli`/`wasm-pack`) is explicitly not invoked; `build` remains offline and hermetic.
