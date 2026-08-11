# Named counterexamples for generics-bounds-and-associated-items

This document preserves invalid or non-compiled counterexamples beside the valid
demonstrations. Only valid source compiles.

## RS-CAN-GEN-001 — Illegal function default

Generic defaults are not permitted on functions. The following is rejected and
not present as source:

```rust
fn illegal_default<T = String>(value: T) {}
```

Valid contrast: `generic_params::Inventory`, `Tagged`, `Repository`,
`DefaultMap`, and `DefaultInventory` use legal defaults on structs, enums,
traits, and type aliases; `generic_params::process` shows a function with
generic parameters but no defaults.

## RS-CAN-GEN-002 — Missing non-implied bound

Most trait obligations are not implied by outlives. The following is rejected:

```rust
trait NeedsClone {}
fn requires_clone<T: NeedsClone>(value: T) where T: Clone {}
fn call<T>(value: T) { requires_clone(value); } // error: T: Clone not implied
```

Valid contrast: `bounds::Holder` demonstrates an implied `T: 'a` via `&'a T`
without an explicit `where T: 'a`; `bounds::projection_bound` shows an explicit
associated projection bound `T::Output: Display` that must be written.

## Leak-check failure

Higher-ranked lifetimes must not leak a concrete lifetime into a `for<'a>`
binder. The following fails:

```rust
fn leak<'a>(value: &'a str) -> &'static str {
    // cannot return &'a str as &'static str through HRTB boundary
    apply_for_all(|s| value)
}
```

Valid contrast: `bounds::apply_for_all` and `bounds::invoke_hrtb` accept
callbacks valid for every lifetime `for<'a> Fn(&'a str) -> &'a str`.

## RS-CAN-GEN-003 — Unsupported const expression

Stable const generics allow only restricted const expressions in type position.
The following is rejected on stable:

```rust
fn unsupported<const N: usize>() -> [u8; N + core::mem::size_of::<usize>()] { [0; _] }
```

Valid contrast: `const_generics::Buffer`, `Flag`, `Tag`, and
`const_generics::compile_time_use` use integer, boolean, and character const
params with supported expressions and braces `Buffer<{ 2 + 2 }>`.

## Post-monomorphization failure

Const evaluation can fail only after instantiation:

```rust
struct Even<const N: usize>;
impl<const N: usize> Even<N> where [(); N % 2]: Sized {
    // fails only when N is odd at monomorphization time
}
```

Valid contrast: `const_generics::distinct_instantiations` shows distinct
`Buffer<4>` and `Buffer<8>` instantiations that succeed.

## RS-CAN-GEN-004 — Projection cycle / overflow

Associated type projection can form a cycle or overflow the trait solver:

```rust
trait Cycle { type Assoc: Cycle; }
// impl Cycle for () { type Assoc = (); } // cycle if Assoc projects to Self
```

Valid contrast: `associated::Record` and `associated::Transform` show
well-formed associated types with shorthand `T::Key` and fully qualified
`<T as Record>::Key` and `::VERSION`.

## RS-CAN-GEN-005 — Rejected lifetime substitution for GAT

A GAT requiring `where Self: 'a` rejects substitution where `Self` does not
outlive `'a`:

```rust
fn rejected<'a>(store: Store) -> Store::Item<'a> where Store: 'a { store.get_for::<'a>() }
// fails if Store does not live long enough
```

Valid contrast: `gat::Lending` defines `type Item<'a> where Self: 'a` and
`gat::borrow_item` shows the required bound at the consumer.

## RS-CAN-GEN-006 — Ambiguous multi-input elision

Elision with multiple input lifetimes and one output is ambiguous:

```rust
fn ambiguous(a: &str, b: &str) -> &str { a } // error: multiple input lifetimes
```

Valid contrast: `elision::first_word` (single input) elides successfully;
`elision::longer` provides explicit `'a` for multiple inputs; trait-object
defaults `Box<dyn Summary>` vs `Box<dyn Summary + '_>` appear in `elision`.

## RS-CAN-GEN-007 — Rejected lifetime substitution via invariance

Covariant substitution is accepted but invariant substitution is rejected:

```rust
fn rejected_invariant<'a, 'b>(cell: Cell<&'a str>) -> Cell<&'b str> where 'a: 'b {
    cell // error: Cell is invariant
}
```

Valid contrast: `variance::covariant_substitution` and
`variance::accepted_substitution` show covariant `&'a T` and
`PhantomData<&'a T>` acceptance; `variance::RawConst` documents
`PhantomData<*const T>` auto-trait effects; `variance::invariant_demo` does not
perform the illegal coercion.

## RS-CAN-GEN-008 — Precise capture restrictions

Precise capture `use<...>` has restrictions:

```rust
trait Restricted {
    fn method<T>(&self, value: T) -> impl Clone + use<T>; // error: trait methods cannot use precise capture in stable position
    fn apti(value: impl Clone) -> impl Clone + use<>; // APTI position cannot capture like RPIT
}
```

Valid contrast: `precise_capture` (edition 2024) and `crates/capture-2021`
(edition 2021) show `use<'a>`, `use<T>`, `use<N>`, `use<>`, `use<'a, T, N>`
with lifetime, type, and const captures, and `default_capture_2024` vs
`legacy_default_capture` contrast the edition defaults.
