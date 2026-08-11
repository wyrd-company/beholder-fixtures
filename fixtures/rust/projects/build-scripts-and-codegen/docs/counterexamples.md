# Counterexamples (documentation only)

These invalid or failing cases are preserved as documentation beside valid
demonstrations. No counterexample is compiled as source in this fixture.

## RS-CAN-PROJ-011 — Build-script protocol

### Build-script panic
A build script that panics aborts the compilation before any `cargo:` directives
are processed. The valid build scripts in `build.rs` and
`crates/fixture-native-sys/build.rs` never panic; they exit normally and emit
directives. A panic would surface as a build failure with no generated artifacts.

### Unexpected-cfg warning
If a build script emits `cargo:rustc-cfg=fixture_unexpected` without a matching
`cargo:rustc-check-cfg=cfg(fixture_unexpected)`, the compiler would warn
`unexpected_cfgs` (see `check-cfg` documentation). This project emits every cfg
with a preceding `cargo:rustc-check-cfg` to avoid the warning, as demonstrated
in `build.rs` (`fixture_build_cfg`, `host_target_match`, `fixture_conditional`)
and `crates/fixture-native-sys/build.rs` (`native_available`).

### Changed generated result without source-tree Rust edit
Demonstrated by `FIXTURE_GENERATED_SEED` influencing `OUT_DIR/generated_items.rs`
and `OUT_DIR/generated_expression.rs`. Changing the environment variable
produces different `GENERATED_CONST` without editing tracked source. A naive
generator that ignores `rerun-if-env-changed` would not rebuild when the
environment changes.

### Host/target probe conditional output
`HOST` and `TARGET` are available only inside build scripts. Conditional output
( e.g., `host_target_match` cfg and `FIXTURE_HOST`/`FIXTURE_TARGET` env) varies
when cross-compiling to `aarch64-unknown-linux-gnu`. On this host build
`HOST == TARGET`, so `host_target_match` is active. Building with
`--target aarch64-unknown-linux-gnu` would make the else-branch valid.

## RS-CAN-PROJ-012 — Generated Rust and include-family

### Missing generated output
`include!(concat!(env!("OUT_DIR"), "/missing.rs"))` would fail at compile time
with "no such file or directory" if the build script did not emit the file. The
valid includes in `src/lib.rs` reference files that `build.rs` guarantees to
generate before compilation.

### Syntax-context mismatch
`include!` parses the included file in the caller's syntactic context. Including
item-level Rust (`pub struct ...`) inside an expression position, or an expression
(`42 + 1`) at module item level, fails to parse. Valid code places
`generated_items.rs` at item scope and `generated_expression.rs` inside a
function body returning `u32`.

### Diagnostics pointing to generated files
A syntax error inside `OUT_DIR/generated_items.rs` would report the generated
path in compiler diagnostics. This project's generated files are valid Rust, so
no diagnostic path remapping is exercised beyond the successful inclusion.

### Relative vs OUT_DIR include paths
`include!("included_relative.rs")` resolves relative to `src/lib.rs`, while
`include!(concat!(env!("OUT_DIR"), "/generated_items.rs"))` resolves via an
absolute path to `OUT_DIR`. Mixing the bases (e.g., using `OUT_DIR` literal
without `env!` or using relative `../target/...`) would break offline or
cross-workspace builds.

### One file both included and module-mounted
`src/dual_source.rs` is mounted as `mod dual_mounted` and also included via
`include!("dual_source.rs")` in `dual_included`. The two `DualType` definitions
are distinct nominal types; assigning one to the other fails type checking even
though the textual source is identical. The same holds for generated file
`dual.rs` included in two modules.

## RS-CAN-PROJ-020 — Native links ownership and build metadata

### Duplicate links claim
Two crates in one graph with `links = "fixture_native"` would fail with
"multiple packages link to native library `fixture_native`". Only
`crates/fixture-native-sys` declares `links = "fixture_native"` in this workspace.

### Metadata not reaching an ordinary crate
`cargo:fixture_kind=native` emitted by `fixture-native-sys` is available only
to direct dependent *build scripts* as `DEP_FIXTURE_NATIVE_FIXTURE_KIND`, not as
`option_env!` in ordinary crate source. This is demonstrated by
`DEP_NOT_IN_ENV` in `src/lib.rs` being `None` while `build.rs` successfully
reads `DEP_FIXTURE_NATIVE_FIXTURE_KIND` and forwards it as
`CONSUMED_NATIVE_KIND`. The link `#[cfg]` similarly is not forwarded to ordinary
crates.

### Build-script override
A dependent crate's `.cargo/config.toml` or `[replace]` could override the
`fixture-native-sys` build script via `cargo:links` override, but no such
override is present here. The default metadata propagation is demonstrated.

### Cross-compilation configuration
When cross-compiling, a `links` package may emit target-specific metadata
(e.g., separate `TARGET` env handling). This fixture builds in the default
`x86_64-unknown-linux-gnu` context; cross-compilation would exercise the same
conditional metadata paths via host/target probing logic present in both build
scripts.

## RS-CAN-ECO-004 — Build-time native generator

### Missing compiler / header / libclang
`cc::Build::new().file("native/native.c")` requires `cc`/`gcc` 15.2.0 and the
hermetic vendor source. If the toolchain were absent, compilation would fail
with "failed to find tool" or header not found. The vendored `native/native.c`
and `native/native.h` are tracked source; the compiled static archive is an
`OUT_DIR` artifact.

### Generator drift
Checked-in generator source (`native/native.c`, `build.rs`, `vendor/cc`) versus
build-time output (`OUT_DIR/libfixture_native.a`) - drift would occur if the
generated archive were tracked. Here only generator source is tracked; the
artifact regenerates during `build`.

### Vendored vs system feature
A non-hermetic build might use `pkg-config` or system `libfixture_native`. This
project compiles the vendored translation unit hermetically and does not invoke
`pkg-config` or link a system library.

## General

All counterexamples above are documentation only. Valid demonstrations for each
checklist item remain compilable under the declared contexts.
