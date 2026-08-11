# Counterexamples (documentation only — never compiled)

Invalid Rust programs are not part of the corpus. Each item below is the
counterexample that would fail beside the valid demonstration referenced.

## RS-CAN-TYPE-001 — struct private-field construction
```rust,ignore
// Private field external construction/update through a literal is rejected.
let external = PrivateFields { public: 1, private: "x".into() };
let updated = PrivateFields { public: 2, ..external };
```

## RS-CAN-TYPE-002 — duplicate / overflow discriminants, fieldless cast restriction
```rust,ignore
enum Bad { A = 1, B = 1 } // duplicate discriminant rejected
enum Overflow { Max = 255, Next } // overflow of repr type rejected
enum Data { Tuple(i32) }
let _ = Data::Tuple(5) as i32; // data-bearing enum cannot use `as` integer cast
```

## RS-CAN-TYPE-003 — non-Copy union field, pattern, inactive read
```rust,ignore
union Bad { s: String } // ordinary non-Copy field rejected; use ManuallyDrop
// Valid union pattern specifies exactly one field and requires unsafe access:
// unsafe { match u { CopyUnion { as_u32: v } => { let _ = v; } } }
// Invalid: `CopyUnion { as_u32: a, as_i32: b }` (multiple fields) or `CopyUnion {}` (zero fields) is rejected.
// Reading an inactive field or a field whose bit pattern is invalid for the type is UB and never executed.
```

## RS-CAN-TYPE-004 — recursive alias and alias-constructor limit
```rust,ignore
type Rec = Vec<Rec>; // recursive alias without indirection rejected
type Alias = Vec<String>;
let _ = Alias(vec![]); // type aliases have no constructor path; `Vec::new()` is required
```

## RS-CAN-TYPE-005 — index panic and invalid by-value DST
```rust,ignore
let arr = [1, 2, 3];
let _ = arr[10]; // runtime panic (bounds check) not executed in valid fixture
let _value: str = *"harvest"; // `str` cannot be taken by value
let _slice: [u8] = *b"field"; // `[T]` cannot be taken by value
```

## RS-CAN-TYPE-006 — packed, dangling, null, aliasing references
```rust,ignore
#[repr(packed)] struct P { a: u8, b: u32 }
let p = P { a: 0, b: 1 };
// let r: &u32 = &p.b; // creating an unaligned reference is UB
let ptr: *const i32 = std::ptr::null();
let _ = unsafe { *ptr }; // null dereference never executed
// Borrow-violating aliasing through raw pointers is documented but never executed.
```

## RS-CAN-TYPE-007 — capturing closure coercion
```rust,ignore
let base = 10;
let capturing = move |x| x + base;
let _bad: fn(i32) -> i32 = capturing; // capturing closure cannot coerce to `fn`
```

## RS-CAN-TYPE-008 — DST locals / non-final DST field
```rust,ignore
// let value: str; // sized-bound rejected
struct Bad { prefix: [u8], suffix: u8 } // DST must be trailing field
```

## RS-CAN-TYPE-009 — incompatible dyn traits and two non-auto principals
```rust,ignore
trait Bad { fn generic<T>(&self, _: T); }
// dyn Bad is not dyn-compatible (generic method).
trait A {} trait B {}
// dyn (A + B) where both are non-auto principal traits is not allowed.
```

## RS-CAN-TYPE-010 — RPIT hidden-type mismatch and turbofish
```rust,ignore
fn a() -> impl Iterator<Item=i32> { 0..3 }
fn b() -> impl Iterator<Item=i32> { vec![1,2].into_iter() }
// let mixed: Vec<i32> = a().chain(b()).collect(); // distinct hidden types
// let explicit = a::<i32>(); // cannot turbofish an RPIT return
```

## RS-CAN-TYPE-011 — dyn with native async/RPIT trait methods
```rust,ignore
trait WithAsync { async fn run(&self); }
// let _bad: &dyn WithAsync; // native async method makes trait not dyn-compatible without boxing
trait WithRpit { fn make(&self) -> impl Iterator<Item=i32>; }
// let _bad2: &dyn WithRpit; // RPIT method likewise prevents dyn use
```

## RS-CAN-TYPE-012 — direct recursion, alias/layout cycles
```rust,ignore
struct Direct(Direct); // infinite size rejected
type RecAlias = Box<RecAlias>; // recursive alias rejected; use struct indirection
```

## RS-CAN-TYPE-013 — packed unaligned reference and transparent eligibility
```rust,ignore
#[repr(packed)] struct P { a: u8, b: u32 }
fn bad(p: &P) -> &u32 { &p.b } // unaligned reference is UB; copy instead
#[repr(transparent)] struct Bad(u8, u8); // transparent requires single non-zero field
```

## RS-CAN-TYPE-014 — unconstrained ambiguous inference
```rust,ignore
let ambiguous = "hi".parse(); // unconstrained inference ambiguous without target annotation
```

## RS-CAN-TYPE-015 — coercion outside a coercion site
```rust,ignore
fn takes_str(s: &str) {}
let owned: String = "hi".into();
// let mismatch = takes_str; mismatch(owned); // no coercion at ordinary argument position without expected type
let boxed: Box<String> = Box::new("hi".into());
// let thin: &str = *boxed; // `*boxed` as value position has different coercion rules than `&boxed`
```

## RS-CAN-TYPE-016 — invalid `as` casts
```rust,ignore
enum Data { Payload(String) }
let _ = Data::Payload("hi".into()) as i32; // non-fieldless enum cast rejected
let r: &i32 = &5;
// let addr = r as usize; // reference-to-integer requires raw pointer cast, not direct `as usize`
```

## Additional invalid bit-pattern / reference cases
Invalid `char`/`bool` bit patterns, zeroed `NonNull`, misaligned references, and
inactive union reads are documented but never executed, per the brief.
