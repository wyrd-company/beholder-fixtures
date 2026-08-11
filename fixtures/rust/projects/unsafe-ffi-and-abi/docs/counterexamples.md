# Counterexamples (documentation only — never compiled)

Invalid Rust programs are not part of the corpus. Each item below is the
counterexample that would fail or invoke undefined behavior beside the valid
demonstration referenced.

## RS-CAN-UNSAFE-001 — unsafe surface
```rust,ignore
// Missing unsafe marker on an unsafe operation is rejected.
let p: *const i32 = &42;
let _ = *p; // requires `unsafe { *p }`

// Unnecessary `unsafe` on safe code is linted / misleading.
unsafe { let x = 1 + 2; }

// Wrong unsafe impl marker.
struct X;
impl UnsafeMarker for X { fn describe(&self) -> &'static str { "x" } } // `unsafe trait` requires `unsafe impl`

// Safe vs unsafe trait methods: calling via safe wrapper without unsafe block,
// vs unsafe-trait method that still requires safe wrapper contract.

// Edition 2024 explicit unsafe block inside an unsafe fn is linted.
// pub unsafe fn foo(p: *const i32) { *p } // must be `unsafe { *p }` inside.
```

## RS-CAN-UNSAFE-002 — validity and MaybeUninit
```rust,ignore
// Zeroed reference, invalid enum discriminant, or bool/char outside valid range.
let _bad_ref: &u32 = unsafe { core::mem::zeroed() }; // invalid reference, UB if executed
let _uninit: u32 = unsafe { core::mem::MaybeUninit::<u32>::uninit().assume_init() }; // uninitialized read, UB
// Assume init before all fields valid is UB.
// Padding byte comparison via `memcmp` is not valid; only defined field equality is reliable.
```

## RS-CAN-UNSAFE-003 — provenance and addresses
```rust,ignore
// Fabricated reference from arbitrary address without exposing provenance.
let ptr = 0x1234 as *const u32;
let _bad: &u32 = unsafe { &*ptr }; // dangling / unprovenanced, UB

// Out-of-bounds arithmetic beyond allocation (including overflow),
// dereferencing one-past pointer, or aliasing mutable references.

// Wrapping offset is not in-bounds and cannot be used to claim in-bound provenance.
// Miri-detected provenance violations remain observations, not final language law
// beyond the documented stable APIs (`addr`, `with_addr`, `map_addr`,
// `expose_provenance`, `without_provenance`, `with_exposed_provenance`).
```

## RS-CAN-UNSAFE-004 — transmute
```rust,ignore
let a: u32 = 1;
// let _bad: u64 = unsafe { core::mem::transmute(a) }; // size mismatch rejected
// let _bad_ref: &u8 = unsafe { core::mem::transmute(&42u32 as *const u32) }; // invalid bit-pattern / reference validity
// Valid wrapper transmute is only justified for `repr(transparent)` with same
// size/alignment/validity; endianness, `transmute_copy`, padding, and niche
// invalid values are not executed.
```

## RS-CAN-FFI-001 — foreign blocks and ABI strings
```rust,ignore
extern "C" { fn printf(format: *const u8, ...); } // edition 2024 requires `unsafe extern "C"`
// Target-unsupported ABI such as `extern "avr-interrupt"` on x86_64 is rejected.
// Mismatched declaration (e.g., declaring `fn foo(x: u32)` when the foreign
// symbol is `fn foo(x: *mut u8)`) is not a Rust type error but UB at runtime.
// Missing link symbol fails at link time, not during type checking.
```

## RS-CAN-FFI-002 — export names, sections, link identities
```rust,ignore
#[unsafe(export_name = "dup")] pub extern "C" fn a() {}
#[unsafe(export_name = "dup")] pub extern "C" fn b() {} // duplicate symbol rejected by linker
// Wrong architecture native library or missing `#[used]` causing section
// elimination by `staticlib`/`dylib` dead-code elimination are not executed.
// `#[unsafe(link_section = ".my_section")]` without `#[used]` may be removed.
```

## RS-CAN-FFI-003 — FFI-safe layouts
```rust,ignore
// Ordinary Rust enum, `&T`, tuples, or `dyn Trait` across FFI are not defined.
pub extern "C" fn bad(e: Result<u32, ()>) {} // `Result` lacks C ABI contract
// bool/char invalid bit-pattern (e.g., `bool` as `2`), platform-dependent
// `c_int` width, allocator mismatch across ownership boundaries, and use of
// `char`/`bool` where foreign code supplies out-of-range bits are UB.
```

## RS-CAN-FFI-004 — unwinding across ABI
```rust,ignore
extern "C" fn may_panic() { panic!("crosses C ABI"); } // unwinding through `extern "C"` is UB
// Must use `extern "C-unwind"` for unwinding callbacks and catch at the
// boundary with `std::panic::catch_unwind`. Foreign exceptions through Rust
// frames and unsupported `C-unwind` on some targets are not executed.
// `UnwindSafe` advisory bound is documented but not relied upon as a gate.
```

## RS-CAN-FFI-005 — assembly and target features
```rust,ignore
core::arch::asm!("invalid_reg {0}", out("not_a_reg") _); // invalid register rejected
#[target_feature(enable = "unsupported_foo")] unsafe fn bad() {} // unsupported feature rejected
// Calling a `target_feature`-gated function without runtime detection /
// correct `-C target-feature` is UB. `global_asm!` with wrong syntax or
// clobbering the wrong ABI via `asm!` options can cause UB. Portable SIMD /
// nightly-only intrinsics are not used.
```

## RS-CAN-PROJ-017 — no_std, alloc, runtime contracts
```rust,ignore
#![no_std]
// Missing `#[panic_handler]` for a freestanding binary is rejected.
// Duplicate `#[panic_handler]` or `#[global_allocator]` across linked crates is rejected.
#[panic_handler] fn p1(_: &PanicInfo) -> ! { loop {} }
#[panic_handler] fn p2(_: &PanicInfo) -> ! { loop {} } // second handler duplicate

// `std`-only items (e.g., `std::fs`) inside `#![no_std]` without `std` feature fail.
// Accidental feature unification pulling `std` into a `no_std` crate via
// `Cargo.toml` feature forwarding is documented but not linked in the fixture.
// `#![no_core]` and custom language items remain unstable and are not used.
```
