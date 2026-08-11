# Counterexamples (documentation only)

These invalid or failing cases are preserved as documentation beside valid
demonstrations. No counterexample is compiled as source in this fixture.

## RS-CAN-TEST-001 — Unit vs integration crate boundaries

### Private item rejected from integration test
Integration test crates are external crates that see only the public API.
The following fails if placed in `tests/integration_basic.rs`:

```rust
use tests_and_documentation::private_api::private_helper;
// error[E0603]: module `private_api` is private
let _ = private_helper();
```

Valid contrast: `src/lib.rs` unit tests `unit_tests::unit_accesses_private_ancestor`
access the private ancestor `private_api::private_helper` because unit tests
compile inside the crate.

### Accidental helper target discovery
A file at `tests/common.rs` or `tests/helper.rs` would be auto-discovered as an
integration test target (`cargo test` builds `tests/*.rs` at top level). Placing
shared helpers at `tests/common/mod.rs` avoids discovery, since only `tests/*.rs`
directly under `tests/` becomes a target. Documented valid location:
`tests/common/mod.rs`.

### Same helper compiled per integration crate
`tests/common/mod.rs` is included via `mod common;` in both `integration_basic`
and `integration_storage`. Each integration crate compiles its own copy of the
helper; there is no shared crate instance. Changing the helper requires rebuilding
both integration targets.

### Dev dependencies missing cfg(test)
`cfg(test)` is set on the crate under test, not on dependencies. A dev-dependency
would not observe `cfg(test)` if inspected from its own source, which is why
`src/lib.rs::test_only_flag` toggles on `cfg(test)` directly rather than via a
dependency probe.

## RS-CAN-TEST-002 — Harness attributes and generated mains

### Signature restrictions
`#[test]` functions must have signature `fn()`, `fn() -> Result<(), E: Debug>`, or
equivalent with no parameters. The following is rejected:

```rust
#[test]
fn with_args(x: u32) { let _ = x; }
// error: `#[test]` function must not have parameters
```

Valid contrast: `src/lib.rs::harness_tests::passing` (`fn()`),
`result_demo` (`fn() -> Result<(), String>`).

### Panic-abort harness conflict
Setting `panic = "abort"` in a profile would make `#[should_panic]` unreachable,
since the harness expects unwinding. The valid harness in this fixture uses the
default `panic = "unwind"`; `harness_tests::panics` demonstrates a passing
`#[should_panic]` under unwinding.

### Ignored-but-compiled
`#[ignore]` does not prevent compilation. `harness_tests::ignored_demo` compiles
under `cargo test` and is reported as ignored without execution.

### Nightly `#[bench]` rejection
The unstable `#[bench]` attribute requires nightly and is not used here. Stable
benchmarks use `[[bench]] harness = false` with an explicit main, as in
`benches/bench_demo.rs`.

## RS-CAN-TEST-003 — Documentation tests

### compile_fail variant (invalid-only)
The `compile_fail` doctest is intentionally non-compiling synthetic Rust and is
kept as a counterexample, not planned corpus source:

```rust,compile_fail
fn broken() { let x: u32 = "not a u32"; }
```

No such block is present in compiled source; a passing harness does not make it
valid. The runnable, no-run, ignored, should-panic (valid source that panics at
runtime), hidden-line, edition-tagged, and README-inclusion variants are the
planned valid demonstrations in `src/docs.rs` and `src/lib.rs`.

### README drift failure
If `README.md` contained a stale fence that no longer type-checked, the crate-level
`#![doc = include_str!("../README.md")]` inclusion would fail the doctest suite.
The valid README at `README.md` contains a runnable block that matches the public API.

### Synthetic crate injection
`rustdoc` synthesizes a crate and main for each fence; `?` hidden tails and
private accessibility inside the synthetic crate follow normal Rust rules. The
valid hidden-line demonstrations in `src/docs.rs` exercise this model.
