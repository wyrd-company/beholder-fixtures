# Vendored dependency provenance

Third-party crates are pinned in `Cargo.lock`, vendored under `vendor/`, and
resolved offline via `.cargo/config.toml`. No vendored crate is shared with
another fixture project.

| Crate | Version | Source location | License |
| --- | --- | --- | --- |
| serde | 1.0.219 | https://github.com/serde-rs/serde | MIT OR Apache-2.0 |
| serde_derive | 1.0.219 | https://github.com/serde-rs/serde | MIT OR Apache-2.0 |
| thiserror | 2.0.12 | https://github.com/dtolnay/thiserror | MIT OR Apache-2.0 |
| thiserror-impl | 2.0.12 | https://github.com/dtolnay/thiserror | MIT OR Apache-2.0 |
| proc-macro2 | 1.0.107 | https://github.com/dtolnay/proc-macro2 | MIT OR Apache-2.0 |
| quote | 1.0.47 | https://github.com/dtolnay/quote | MIT OR Apache-2.0 |
| syn | 2.0.119 | https://github.com/dtolnay/syn | MIT OR Apache-2.0 |
| unicode-ident | 1.0.24 | https://github.com/dtolnay/unicode-ident | (MIT OR Apache-2.0) AND Unicode-DFS-2016 |

Each vendored directory retains upstream `LICENSE-*` files and
`.cargo-checksum.json` metadata required for offline Cargo resolution.
