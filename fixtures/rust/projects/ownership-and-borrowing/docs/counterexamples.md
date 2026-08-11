# Counterexamples for ownership-and-borrowing

This document preserves invalid or non-compiled counterexamples beside the valid demonstrations in source.
Only valid source compiles in the fixture corpus.

## Whole-value use after move (RS-CAN-OWN-001)

Whole-value use after a field has been moved is rejected:

```rust
let inv = Inventory { name: String::from("x"), quantity: 1, label: String::from("y") };
let Inventory { name, .. } = inv;
let _ = inv; // error[E0382]: use of moved value
let _ = name; // `name` moved here
```

Valid contrast: `src/moves_partial_moves.rs` `destructure_move_and_borrow` and `partial_move_remaining_usable`
move one field while borrowing/copying another and continue using unaffected paths.

## Conflicting simultaneous borrows (RS-CAN-OWN-002)

Simultaneous mutable and shared borrows are rejected:

```rust
let mut data = vec![1, 2, 3];
let r1 = &data;
let r2 = &mut data; // error[E0502]: cannot borrow as mutable because it is also borrowed as immutable
let _ = (r1, r2);
```

Mutable-to-shared reborrow is valid via `&*mut_ref`; see `src/borrow_exclusivity.rs` `mutable_to_shared_reborrow`.

## Non-lexical lifetime live branch (RS-CAN-OWN-003)

If a shared borrow is kept live through a branch, mutation in that branch is rejected:

```rust
let mut data = vec![1, 2, 3];
let r = &data;
// branch where `r` stays live
if cond { println!("{}", r[0]); }
data.push(4); // error if `r` is considered live across the mutation due to branch
```

Valid contrast: `src/nll_two_phase.rs` `nll_mutate_after_last_use` mutates after last use, while `nll_branch_live` keeps borrow live in one branch.

## Explicit mutable borrow in two-phase position (RS-CAN-OWN-003)

Explicit `&mut` argument evaluation that conflicts with a reserved autoref borrow is rejected:

```rust
let mut v = vec![1, 2, 3];
let r = &mut v;
v.push(r.len()); // error[E0502] if `r` were used as explicit argument alongside autoref
```

Valid contrast: `src/nll_two_phase.rs` `two_phase_push_len` with `vec.push(vec.len())` reserves `&mut vec` before evaluating `vec.len()` shared borrow.

## Lock-guard temporary hazard (RS-CAN-OWN-004)

Binding a lock guard's temporary to `let _ = &Mutex::lock()` does not extend its lifetime; the guard drops immediately:

```rust
let _ = &Mutex::new(1).lock().unwrap();
// temporary guard dropped here, not at scope end
```

Valid contrast: `src/temporary_scopes.rs` `extending_borrow` vs `nonextending_borrow` demonstrates extending `let x = &String::from(...)` vs non-extending `let _ = &String::from(...)`.

## Destruction order borrow rejection (RS-CAN-OWN-004 / RS-CAN-OWN-010)

A borrow that does not outlive the value's destruction order is rejected:

```rust
struct Holder<'a> { r: &'a i32 }
let val = {
    let x = 5;
    Holder { r: &x } // error: `x` does not live long enough
};
```

Valid contrast: `src/temporary_scopes.rs` `destructor_order_inner` and edition-2021 crate demonstrate drop order without borrowing across destruction.

## RefCell runtime panic (RS-CAN-OWN-005)

`RefCell` enforces borrow rules at runtime; conflicting borrows panic:

```rust
let rc = RefCell::new(1);
let _a = rc.borrow();
let _b = rc.borrow_mut(); // panic: already borrowed
```

Valid contrast: `src/interior_mutability.rs` `refcell_success` uses non-overlapping borrows, `refcell_try_conflict` uses `try_borrow_mut` to detect without panic, and `refcell_panicking_caught` catches the panic via `catch_unwind`.

## Whole vs disjoint closure capture (RS-CAN-OWN-006)

In edition 2018, disjoint field capture was not precise; capturing one field borrowed the whole struct:

```rust
// edition 2018: captures whole `pair`, so mutation of disjoint field is rejected
let mut pair = Pair { first: String::from("a"), second: String::from("b") };
let c = || pair.first.len();
pair.second.push_str("!"); // error in 2018, accepted in 2021
let _ = c();
```

Valid contrast: `crates/edition-2018/src/lib.rs` `capture_2018_whole` avoids disjoint mutation while closure is live; `crates/edition-2021/src/lib.rs` `capture_2021_disjoint` succeeds in 2021.

## Inconsistent or-binding (RS-CAN-OWN-009)

Or-pattern alternatives must bind the same names with same types:

```rust
match (1, 2) {
    (a, 2) | (1, b) => println!("{} {}", a, b), // error: inconsistent bindings
    _ => {}
}
```

Valid contrast: `src/binding_modes.rs` `or_pattern_agreement` and `src/patterns.rs` `tuple_slice_range_or_guarded` use `Some(1) | Some(2)` with consistent bindings.

## Refutable pattern in irrefutable context (RS-CAN-OWN-009)

Irrefutable `let` cannot use a refutable pattern without diverging else:

```rust
let Some(x) = Some(1); // warning/error: refutable pattern in local binding, use `if let` or `let-else`
```

Valid contrast: `src/patterns.rs` `let_else_pattern` uses `let Some(value) = opt else { return -1; }`, `if_let_pattern` uses `if let`, and `let_patterns` uses irrefutable tuple/struct patterns.

## Borrow rejected by destruction order / Phantom drop check (RS-CAN-OWN-010)

Generic wrapper with `PhantomData<T>` and `Drop` requires `T` outlives wrapper; a borrow that would be invalidated by drop is rejected:

```rust
struct Owning<T> { ptr: *const T, _m: PhantomData<T> }
impl<T> Drop for Owning<T> { fn drop(&mut self) {} }
let short;
let owning = Owning::new(&short /* temporary */); // error: borrowed value does not live long enough
```

Valid contrast: `src/destructuring_assignment.rs` `Owning` vs `NonOwning<'a, T>` with `PhantomData<&'a T>` and `Drop` demonstrates drop-check-appropriate phantom ownership.

## Illegal destructuring assignment pattern (RS-CAN-OWN-010)

Binding forms like `ref` or type ascriptions are legal in `let` but not in assignment:

```rust
let mut a = 1;
let mut b = 2;
(ref a, b) = (1, 2); // error: `ref` not allowed in assignment
(a, b): (i32, i32) = (3, 4); // error: type ascription not allowed in assignment left-hand side
```

Valid contrast: `src/destructuring_assignment.rs` `nested_destructuring_assignment` uses place-expression assignment `(a, b) = (10, 20)` and `let_only_pattern` shows the valid `let ref value` form.

## Edition 2024 explicit binding mode restriction (RS-CAN-OWN-008)

In edition 2024, explicit `ref`/`ref mut` under an inherited reference binding mode is restricted:

```rust
// edition 2024: inherited mode is already `ref` due to `&container` scrutinee
match &container {
    Container { ref value, .. } => {} // warning/error in 2024, allowed in 2021
}
```

Valid contrast: `src/binding_modes.rs` (2024) uses inferred binding modes for `&container` matches, while `crates/edition-2021/src/lib.rs` `explicit_binding_modes_2021` demonstrates the valid 2021 explicit `ref` pattern.
