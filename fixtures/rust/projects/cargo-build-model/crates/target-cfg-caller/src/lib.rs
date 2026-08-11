//! RS-CAN-PROJ-008: target-specific dependency tables selected by cfg and exact triples.
//! Common caller that selects dependencies via cfg predicates and exact triple.

#[cfg(unix)]
pub fn caller_platform() -> &'static str {
    target_unix_dep::platform()
}

#[cfg(windows)]
pub fn caller_platform() -> &'static str {
    target_windows_dep::platform()
}

#[cfg(not(any(unix, windows)))]
pub fn caller_platform() -> &'static str {
    "other"
}

#[cfg(target_arch = "x86_64")]
pub fn caller_arch() -> &'static str {
    target_arch_dep::arch()
}

#[cfg(not(target_arch = "x86_64"))]
pub fn caller_arch() -> &'static str {
    "other-arch"
}

#[cfg(target_os = "linux")]
pub fn caller_os() -> &'static str {
    target_os_dep::os()
}

#[cfg(not(target_os = "linux"))]
pub fn caller_os() -> &'static str {
    "other-os"
}

// Exact triple: `[target.x86_64-unknown-linux-gnu.dependencies]` in Cargo.toml
// selects `target-triple-dep` only when compiling for that literal triple
// string. `cfg(target = "...")` is not a real rustc cfg key (rustc has no
// `target` key; see `target_arch`/`target_os`/`target_env`/etc.), so the
// common caller instead reaches the exact-triple edge with the combination of
// real, stable cfg keys that uniquely identifies x86_64-unknown-linux-gnu
// (`rustc --print cfg` on this host: target_arch="x86_64", target_os="linux",
// target_env="gnu").
#[cfg(all(target_arch = "x86_64", target_os = "linux", target_env = "gnu"))]
pub fn caller_triple() -> &'static str {
    target_triple_dep::triple()
}

#[cfg(not(all(target_arch = "x86_64", target_os = "linux", target_env = "gnu")))]
pub fn caller_triple() -> &'static str {
    "other-triple"
}

// Overlapping table merge: unix + x86_64 both active on host, demonstrating merge.
// Unsupported feature predicates in target tables would fail: e.g. `[target.'cfg(feature="x")'.dependencies]`
// is not allowed because feature is not a valid target predicate (counterexample documented).

pub fn caller_summary() -> String {
    format!(
        "{}-{}-{}-{}",
        caller_platform(),
        caller_arch(),
        caller_os(),
        caller_triple()
    )
}
