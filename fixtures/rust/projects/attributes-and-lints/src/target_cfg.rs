//! Built-in target cfg families, declared custom cfg, and unexpected-cfg warning.

/// Summary of major target cfg families observable on the host.
pub fn target_family_summary() -> String {
    let mut parts = Vec::new();
    if cfg!(target_arch = "x86_64") {
        parts.push("arch_x86_64");
    }
    if cfg!(target_os = "linux") {
        parts.push("os_linux");
    }
    if cfg!(target_family = "unix") {
        parts.push("family_unix");
    }
    if cfg!(target_pointer_width = "64") {
        parts.push("pointer_64");
    }
    if cfg!(target_endian = "little") {
        parts.push("endian_little");
    }
    if cfg!(target_env = "gnu") {
        parts.push("env_gnu");
    }
    if parts.is_empty() {
        "target_unknown".to_string()
    } else {
        parts.join("+")
    }
}

/// Branch using declared custom cfg `fixture_custom_cfg`.
#[cfg(fixture_custom_cfg)]
pub fn custom_cfg_label() -> &'static str {
    "fixture_custom_cfg_active"
}

#[cfg(not(fixture_custom_cfg))]
pub fn custom_cfg_label() -> &'static str {
    "fixture_custom_cfg_inactive"
}

/// Unexpected cfg name retained to emit `unexpected_cfgs` warning at compile time.
#[cfg(fixture_unexpected_cfg_name)]
pub fn unexpected_cfg_demo() -> &'static str {
    "unexpected_cfg_branch"
}

/// Mutually exclusive shipped target module branches; only host edge compiles.
#[cfg(unix)]
mod unix_target_module {
    pub fn branch_label() -> &'static str {
        "unix_target_module"
    }
}

#[cfg(windows)]
mod windows_target_module {
    pub fn branch_label() -> &'static str {
        "windows_target_module"
    }
}

/// Host-visible label from the compiled unix target module branch.
#[cfg(unix)]
pub fn exclusive_target_module_label() -> &'static str {
    unix_target_module::branch_label()
}

/// Host-visible label from the compiled windows target module branch.
#[cfg(windows)]
pub fn exclusive_target_module_label() -> &'static str {
    windows_target_module::branch_label()
}

/// Fallback label when neither unix nor windows target modules compile.
#[cfg(not(any(unix, windows)))]
pub fn exclusive_target_module_label() -> &'static str {
    "no_target_module"
}
