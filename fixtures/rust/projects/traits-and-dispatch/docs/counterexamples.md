# Counterexamples for traits-and-dispatch

This document preserves invalid or non-compiled counterexamples beside the valid
demonstrations in source. All fixture source remains valid in the default build
context (`x86_64-unknown-linux-gnu`, edition 2024, stable 1.97.1).

## Foreign-for-foreign impl (RS-CAN-TRAIT-002)

A trait impl where both trait and type are foreign is rejected by coherence:

```rust,ignore
// impl std::fmt::Display for Vec<i32> {} // error: only traits defined in the current crate can be implemented for arbitrary types
```

Valid contrast: `LocalTrait for String` (local trait, foreign type) and
`std::fmt::Display for LocalType` (foreign trait, local type) appear in
`src/coherence.rs`; newtype `Wrapper(Vec<i32>)` wraps the foreign type to allow
a foreign-trait impl.

## Overlapping impl (RS-CAN-TRAIT-002, RS-CAN-TRAIT-003)

Two impls that could apply to the same type overlap and are rejected:

```rust,ignore
trait Overlap {}
impl<T> Overlap for T {}
impl Overlap for i32 {} // error: conflicting implementations
```

Valid contrast: conditional `Replicate for Wrap<T> where T: Clone` and blanket
`ExtLabel for T where T: Display` in `src/conditional.rs` are non-overlapping
and have satisfying (`Wrap<i32>`, `Displayable`) and non-satisfying (`Wrap<Opaque>`, `Opaque`) sites.

## Missing supertrait (RS-CAN-TRAIT-004)

A subtrait requires its supertrait; implementing the subtrait without the supertrait fails:

```rust,ignore
trait Base {}
trait Derived: Base {}
struct S;
impl Derived for S {} // error: the trait bound `S: Base` is not satisfied
```

Valid contrast: `Base` and `Derived: Base` hierarchy with `InheritAll` and
`OverrideDefault` impls in `src/supertrait.rs`; direct qualified calls show
which default body executes.

## Consuming dyn method (RS-CAN-TRAIT-005)

A consuming method on a trait object is rejected even when the trait itself is dyn-safe via `Self: Sized`:

```rust,ignore
trait NeedsSized {
    fn consume(self) -> i32 where Self: Sized;
    fn borrow(&self) -> i32;
}
fn demo(obj: &dyn NeedsSized) {
    let _ = obj.borrow(); // ok
    // obj.consume(); // error: cannot call consuming method on trait object due to `Self: Sized`
}
fn boxed_demo(obj: Box<dyn NeedsSized>) {
    // obj.consume(); // error: same — consuming method requires `Self: Sized`
}
```

Valid contrast: `ReceiverTrait::consume(self) where Self: Sized` and
`boxed(self: Box<Self>) where Self: Sized` in `src/receivers.rs`; the remaining
`&self`/`&mut self`/`Pin<&mut Self>` methods are dyn-compatible and callable through `&dyn ReceiverTrait`.

## `Copy + Drop` rejection (RS-CAN-TRAIT-012)

Implementing `Copy` and `Drop` together is rejected:

```rust,ignore
struct BadCopyDrop;
impl Copy for BadCopyDrop {}
impl Clone for BadCopyDrop { fn clone(&self) -> Self { *self } }
impl Drop for BadCopyDrop { fn drop(&mut self) {} } // error: the trait `Copy` cannot be implemented for this type; the type has a destructor
```

Valid contrast: `Copyable: Copy + Clone` without `Drop` and drop types `Inner`, `Outer`, `Nested` in
`src/drop_semantics.rs`; `ManuallyDrop` and `forget` show suppression without violating the rule.

## Invalid implicit conversion (RS-CAN-TRAIT-011)

No implicit conversion from a primitive to a custom type:

```rust,ignore
struct UserId(u32);
let _id: UserId = 10_u32; // error: mismatched types
```

Valid contrast: explicit `From<u32> for UserId`, `TryFrom<i64> for CheckedId`, reciprocal
`Into` via `accepts_into`, and `?` error conversion in `src/conversion.rs`; the direct assignment remains invalid.

## Direct destructor call (RS-CAN-TRAIT-012)

Calling `Drop::drop` directly is rejected:

```rust,ignore
struct WithDrop;
impl Drop for WithDrop { fn drop(&mut self) {} }
let mut x = WithDrop;
x.drop(); // error: explicit use of destructor method
WithDrop::drop(&mut x); // error: same
```

Valid contrast: explicit `drop(x)` function, `ManuallyDrop`, `forget`, and normal drop glue in
`src/drop_semantics.rs`; destructors run via compiler-generated drop glue, not direct calls.
