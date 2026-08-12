# Named counterexamples for api-facades-and-lazy-globals

This document preserves invalid or non-compiled counterexamples beside the valid
demonstrations in source. Counterexamples are documentation only and are never
present as invalid Rust source in the fixture corpus.

## Downstream sealed implementation failure

A downstream crate cannot implement `CatalogEntry` because the sealed
supertrait is private to the defining crate. The following is rejected by the
compiler and is not present as source:

```rust
struct ExternalEntry;

impl api_facades_and_lazy_globals::sealed::CatalogEntry for ExternalEntry {
    fn label(&self) -> &str {
        "external"
    }
}
```

Valid contrast: `src/sealed.rs` seals `CatalogEntry` through a private
`Sealed` supertrait, and `crates/facade_downstream/src/lib.rs` consumes the
trait without implementing it.

## Extension method ambiguity

Two blanket extension traits that expose the same method name leave the call
site ambiguous when both traits are in scope. The following is rejected by the
compiler with `E0034` and is not present as source:

```rust
trait AlphaExt {
    fn describe(&self) -> &str;
}

trait BetaExt {
    fn describe(&self) -> &str;
}

impl<T> AlphaExt for T {
    fn describe(&self) -> &str {
        "alpha"
    }
}

impl<T> BetaExt for T {
    fn describe(&self) -> &str {
        "beta"
    }
}

struct Entry;

fn ambiguous_call(entry: &Entry) -> &str {
    entry.describe()
}
```

Valid contrast: `src/extension.rs` provides a single blanket `CatalogExt`
implementation without a second in-scope trait method of the same name.

## Lazy global reentrancy or panic path

Initializing a `OnceLock` from within its own initializer can panic on
reentrancy. The following is not present as source:

```rust
static REENTRANT: OnceLock<u32> = OnceLock::new();

fn reentrant_init() -> u32 {
    *REENTRANT.get_or_init(|| reentrant_init())
}
```

Valid contrast: `src/lazy_globals.rs` initializes `OnceLock`, `LazyLock`, and
the legacy `lazy_static!` counter through independent, non-reentrant bootstrap
paths.

## Valid non-conforming API naming

Naming conventions are ecosystem guidance rather than compiler rules. The
following would compile but is intentionally not used in fixture source:

```rust
struct LegacyMetric {
    value: f64,
}

impl LegacyMetric {
    fn get_value(&self) -> f64 {
        self.value
    }
}
```

Valid contrast: `src/naming.rs` uses `value`, `as_ratio`, `to_basis_points`,
and `into_parts` without `get_` prefixes, and derives standard traits on
`Label`.
