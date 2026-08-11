//! RS-CAN-PROJ-018: entry points and helper for rewritten main.

// Demonstrate no_main handling via helper module (binary no_main_demo uses #![no_main])
pub fn entry_points_summary() -> &'static str {
    "entry_points"
}

// Helper for macro-rewritten main: attribute rewrites signature but compiled sig distinct from source
#[macro_host::entry_wrapper]
pub fn demo_entry_wrapper() -> u32 {
    42
}

// Counterexamples documented:
// - missing main failure: a binary crate without `fn main` and without `#![no_main]` fails to compile
// - main nested only in submodule `mod inner { fn main() {} }` must fail (no crate-root main)
// - custom harness/no_main targets must provide their own contract (not shown as build, documented)
