//! RS-CAN-PROJ-018: macro-rewritten main.
//! Source signature appears as plain `fn main()` but attribute rewrites/ wraps it.

use macro_host::entry_wrapper;

#[entry_wrapper]
fn main() {
    println!("rewritten main");
}
