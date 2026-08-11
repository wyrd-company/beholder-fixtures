# Counterexamples (documentation only — never compiled)

Invalid Rust programs are not part of the corpus. Each item below is the
counterexample that would fail beside the valid demonstration referenced.

## RS-CAN-EXPR-003 — incompatible branch types
```rust,ignore
// Incompatible branch values cannot coerce to a common type.
let _bad = if true { 1 } else { "incompatible" };
```

## RS-CAN-EXPR-004 — invalid valued break from while/for
```rust,ignore
// `while` and `for` are unit-valued; a valued break is rejected.
let _bad = while true { break 5; };
let _bad2 = for _ in 0..3 { break 5; };
// Closure/async control boundary: break cannot cross closure.
let closure = || { loop { break; } /* break outside closure rejected */ };
```

## RS-CAN-EXPR-007 — unconditional-panic index (compile-time)
```rust,ignore
let arr = [1, 2, 3];
// Index with compile-time out-of-bounds literal triggers unconditional panic lint.
let _bad = arr[10];
```

## RS-CAN-EXPR-009 — out-of-range literal
```rust,ignore
let _bad: u8 = 300; // out-of-range for u8
let _bad2: u8 = 0xFFF; // hex out-of-range where truncated
let _bad3 = 9999999999999999999999_i32; // overflow literal
let _bad4 = b'\xFF\u{110000}'; // invalid scalar/escape
```

## RS-CAN-CONST-001 — static-mut reference denial under edition 2024
```rust,ignore
static mut COUNTER: i32 = 0;
// Edition 2024 denies creating a shared reference to `static mut`.
let _bad: &i32 = &COUNTER;
let _bad2: &mut i32 = &mut COUNTER;
// Must use raw pointer via `addr_of!` / `addr_of_mut!` outside unsafe or explicitly unsafe block:
let _ok = unsafe { std::ptr::addr_of!(COUNTER).read() };
```

## RS-CAN-CONST-003 — runtime-dependent value that cannot be promoted
```rust,ignore
fn not_promotable(input: i32) -> &'static i32 {
    // Cannot promote a borrow of a runtime-dependent value to `'static`.
    &input
}
```

## RS-CAN-EXPR-001 — invalid assignment target and move-after-move
```rust,ignore
// Not a place; cannot be assignment target.
1 = 2;
*(&3) = 4;
// Move-after-move is rejected for non-Copy.
let s = String::from("once");
let _a = s;
let _b = s;
```

## RS-CAN-EXPR-002 — semicolon inference and item position counterexample
```rust,ignore
// Using a tail without semicolon where unit expected may mis-infer return type.
// Outer attribute on a statement position is rejected:
#[allow(dead_code)] let x = 1;
```

## RS-CAN-EXPR-005 — closure return target counterexample
```rust,ignore
// `return` inside closure targets the closure, not the outer function.
fn outer() -> i32 {
    let closure = || { return 5; };
    closure();
    0
}
```

## RS-CAN-EXPR-006 — mixing Option/Result and Try counterexamples
```rust,ignore
fn demo() -> Result<i32, String> {
    let _bad: Option<i32> = None;
    let _x = _bad?; // `?` in Result fn on Option without conversion rejected (missing FromResidual).
    Ok(0)
}
```

## RS-CAN-EXPR-007 — float pattern and empty/invalid range counterexamples
```rust,ignore
match 1.5 { 0.0..=1.0 => {} } // float range pattern rejected
match 10 { 10..0 => {} } // empty range pattern still valid but never matches; invalid type is rejected
let _bad = "harvest"[0]; // string integer indexing not allowed via Index; use slicing on valid UTF-8 boundaries
```

## RS-CAN-EXPR-008 — panic during operand evaluation and macro-produced counterexample
```rust,ignore
// Panic during one operand still respects left-to-right evaluation order; the later operand is not reached.
fn panic_right() -> i32 { panic!() }
let _bad = 1 + panic_right();
```

## RS-CAN-CONST-002 — evaluated const panic/overflow and generic failure
```rust,ignore
const fn must_not_overflow(a: u8, b: u8) -> u8 { a + b }
// Evaluated branch that overflows in const is rejected at compile time:
const BAD: u8 = must_not_overflow(200, 200);
const fn generic<T>(x: usize) -> usize { x * 2 }
// Generic instantiation that fails const rules after substitution is rejected:
const BAD2: usize = generic::<String>(usize::MAX);
```

## RS-CAN-CONST-003 — destructor-bearing and interior-mut non-promoted values
```rust,ignore
struct WithDrop(String);
impl Drop for WithDrop { fn drop(&mut self) {} }
let _promoted: &'static WithDrop = &WithDrop(String::from("field")); // not promotable due to destructor
let _cell_promoted: &'static std::cell::Cell<i32> = &std::cell::Cell::new(5); // interior mut not promotable
```
