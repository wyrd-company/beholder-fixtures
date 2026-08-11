# Counterexamples (documentation only)

Valid demonstrations are compiled; the following invalid cases are documented as non-compiled examples beside their valid counterparts.

## RS-CAN-MAC-001

- No matching arm: `multi_arm!(1, 2, 3, 4)` has no arm expecting four expressions; expansion fails.
- Follow-set violation: `nested_pairs!(alpha => )` missing expression after `=>`.
- Recursion limit: deeply nested `recursive!` exceeding `recursion_limit`.

## RS-CAN-MAC-002

- Ordering: using `later_macro!()` before its definition in textual scope without prior declaration is rejected since 2021.
- `local_inner_macros` without `#[macro_export(local_inner_macros)]` fails when inner macro calls another.

## RS-CAN-MAC-003

- Private helper failure: macro calling `$crate::helper::private_fn()` where `private_fn` is `fn private()` fails due to visibility even through `$crate`.
- `$crate` does not bypass privacy.

## RS-CAN-MAC-004

- Duplicate generated output: `define_family!(AlphaItem, AlphaItem)` duplicates type name.
- Hidden `$crate::__private` API usage without proper re-export.

## RS-CAN-MAC-005

- Unknown helper without derive: `#[describe(tag = "...")]` without `#[derive(Describe)]` inertly ignored or warned.
- Duplicate `impl` from two derives conflicting.

## RS-CAN-MAC-006

- Expansion panic/loop: attribute macro panicking during expansion aborts compilation.
- Invalid tokens passed to function-like macro.

## RS-CAN-MAC-007

- Call-site span collision: generating `let x = 1;` with `Span::call_site()` when caller already has `let x` duplicates.

## RS-CAN-ECO-009

- Expansion-time invalid input: `inline_dsl!("alpha not_a_number")` emits `compile_error!` via procedural macro.
- Offline file with malformed line emits `compile_error!`.

## RS-CAN-PROJ-018

- Missing main: binary without `fn main` and without `#![no_main]` fails `error: main not found`.
- Main nested in submodule only: `mod m { fn main() {} }` does not satisfy crate root.

## RS-CAN-PROJ-013

- Attempted normal export from `proc-macro` crate (`pub fn normal_fn`) not accessible as ordinary library.
- Host-only dependency not visible to target crate.
