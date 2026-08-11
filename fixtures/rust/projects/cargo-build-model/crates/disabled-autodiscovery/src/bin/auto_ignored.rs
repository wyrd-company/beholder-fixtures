// RS-CAN-PROJ-002: this file is never auto-discovered as a `[[bin]]` because
// `autobins = false` in Cargo.toml disables binary auto-discovery for this
// package; only the explicit `[[bin]] explicit-bin` target is compiled. It is
// valid Rust (the project scope requires checked-in fixture source to be
// controlled valid Rust, not invalid source), and would compile fine as a
// `auto-ignored` binary if `autobins` were re-enabled.
fn main() {
    println!("auto_ignored: would be discovered as a bin named `auto-ignored` if autobins were true");
}
