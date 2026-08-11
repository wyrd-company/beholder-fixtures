# Counterexamples (documentation only — never compiled)

Invalid or omitted Rust programs are not part of the corpus. Each item below is
the counterexample preserved as documentation beside its valid demonstration.

## RS-CAN-ECO-003 — `Send + 'static` spawn requirement

```rust,ignore
// `tokio::spawn` requires the future to be `Send + 'static`. Capturing a
// non-Send `Rc` or a non-'static reference is rejected at compile time.
use std::rc::Rc;
let rc = Rc::new(5);
tokio::spawn(async move { println!("{}", rc); }); // error: `Rc` is not `Send`

let data = String::from("local");
tokio::spawn(async move { println!("{data}") }); // `data` must be 'static if moved into spawn
```

## RS-CAN-ECO-003 — `tracing::instrument` / runtime stacking notes

- Attribute order matters: `#[tokio::main] #[tracing::instrument]` and
  `#[tracing::instrument] #[tokio::main]` expand in opposite wrapper orders.
  Only one order preserves the intended span-across-runtime-boundary semantics.
- Version-specific hidden macro output (the exact generated module name,
  span identifier, or `tokio::runtime::Builder` invocation) is implementation
  detail of `tokio`/`tracing` and is preserved at documentation level rather
  than asserted in fixture source.

## RS-CAN-ECO-007 — dead or unlinked producer omitted from the set

```rust,ignore
// If a producer's crate or object file is never linked (e.g., an optional
// dependency that is not enabled, or a module eliminated by dead code
// elimination / LTO), its `inventory::submit!` never contributes to the
// section and `inventory::iter::<PluginDescriptor>` excludes it.
#[allow(unused)]
static PLUGIN_GHOST: PluginDescriptor = PluginDescriptor { name: "ghost", version: 99 };
inventory::submit!(PLUGIN_GHOST);
// When the `ghost` producer crate is not a dependency of the final binary,
// PLUGIN_GHOST is absent from `inventory::iter`.
```

## RS-CAN-ECO-007 — duplicate registration

```rust,ignore
// Submitting two entries with the same identity that the consumer treats as
// unique (e.g., same `name`) is not prevented by the linker collection — the
// set then contains duplicates and violates the intended uniqueness invariant.
// The registration crate itself deduplicates only by the submission's address,
// not by `PluginDescriptor::name`.
inventory::submit!(PluginDescriptor { name: "alpha", version: 1 });
inventory::submit!(PluginDescriptor { name: "alpha", version: 1 }); // duplicate logical entry
```

## RS-CAN-ECO-007 — platform / linker section notes

- `inventory` uses host ELF linker sections (`__link_section__` / `__used`) on
  `x86_64-unknown-linux-gnu`. The collected set relies on the host ELF linker;
  another target or a fully stripped / LTO-thinned link may retain a different
  set, which is why the fixture's declared context names the ELF host.
- Constructors run before `main`; the `ctor` / `link_section` ordering is also
  implementation-defined.
