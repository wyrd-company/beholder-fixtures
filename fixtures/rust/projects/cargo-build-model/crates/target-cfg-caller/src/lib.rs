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

// Exact triple: only on x86_64-unknown-linux-gnu
#[cfg(target = "x86_64-unknown-linux-gnu")]
pub fn caller_triple() -> &'static str {
    target_triple_dep::triple()
}

#[cfg(not(target = "x86_64-unknown-linux-gnu"))]
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
