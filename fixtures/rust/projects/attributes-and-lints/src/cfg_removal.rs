//! Conditional compilation removal, `cfg_attr`, and `cfg!` boolean checks.

use derive_helpers::DemoDerive;

/// Struct with cfg-gated fields compiled only on the host edge.
pub struct CfgStruct {
    /// Field compiled on unix targets.
    #[cfg(unix)]
    pub unix_field: i32,
    /// Field compiled on windows targets.
    #[cfg(windows)]
    pub windows_field: i32,
}

/// Enum with cfg-gated variants for mutually exclusive target branches.
pub enum CfgEnum {
    /// Unix-only variant.
    #[cfg(unix)]
    UnixArm,
    /// Windows-only variant.
    #[cfg(windows)]
    WindowsArm,
    /// Shared variant on all compiled targets.
    Shared,
}

/// Label selected by active cfg branches on the host.
pub fn cfg_branch_label() -> &'static str {
    if cfg!(unix) {
        "unix_branch"
    } else if cfg!(windows) {
        "windows_branch"
    } else {
        "other_branch"
    }
}

/// cfg on a module with cfg_attr-injected allow attribute.
#[cfg(unix)]
#[cfg_attr(unix, allow(dead_code))]
mod unix_only_module {
    fn unix_only_dead() {}

    pub fn unix_module_label() -> &'static str {
        "unix_only_module"
    }
}

/// cfg_attr injecting a derive helper on a unix-only struct.
#[cfg(unix)]
#[cfg_attr(unix, derive(DemoDerive))]
#[demo_helper(note = "cfg_attr derive injection")]
struct UnixCfgDerive;

#[cfg(unix)]
pub fn unix_cfg_derive_marker() -> &'static str {
    UnixCfgDerive.demo_marker()
}

/// cfg_attr injecting repr on a cfg-gated struct.
#[cfg(unix)]
#[cfg_attr(unix, repr(C))]
struct UnixReprStruct {
    value: u8,
}

/// cfg_attr injecting a module path on the host unix edge.
#[cfg(unix)]
#[cfg_attr(unix, path = "unix_impl_file.rs")]
mod unix_impl_file;

#[cfg(unix)]
/// Label from cfg_attr path-injected module.
pub fn unix_path_module_label() -> &'static str {
    unix_impl_file::path_module_label()
}

/// cfg on impl block for the host unix edge.
#[cfg(unix)]
impl CfgStruct {
    /// Impl method compiled only on unix targets.
    pub fn unix_impl_label(&self) -> &'static str {
        "unix_impl"
    }
}

/// cfg on match arm inside expression context.
pub fn cfg_match_arm_label() -> &'static str {
    match () {
        _ if cfg!(unix) => "unix_match_arm",
        _ if cfg!(windows) => "windows_match_arm",
        _ => "fallback_match_arm",
    }
}

/// cfg in supported subexpression `if` position.
pub fn cfg_if_label() -> i32 {
    if cfg!(unix) { 1 } else { 0 }
}

// Counterexample (documented, not compiled): `cfg!(windows)` referencing windows-only APIs inside a `cfg(windows)` block fails on the host because the cfg branch is removed before name resolution.
// cfg_attr no_std injection is demonstrated in `crates/cfg_attr_no_std` built with `--cfg fixture_no_std_edge`.
