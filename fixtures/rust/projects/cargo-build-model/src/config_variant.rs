//! RS-CAN-PROJ-019: source meaning from invocation and external configuration.
//! One source compiled under two invocation and configuration variants.
//! Checked-in `.cargo/config.toml` supplies `cargo_config_flag` and `target_config_flag`.
//! Additional RUSTFLAGS or `--cfg` can toggle `extra_flag`.

#[cfg(cargo_config_flag)]
pub fn variant() -> &'static str {
    "config-a"
}

#[cfg(not(cargo_config_flag))]
pub fn variant() -> &'static str {
    "config-b"
}

#[cfg(extra_flag)]
pub fn extra() -> bool {
    true
}

#[cfg(not(extra_flag))]
pub fn extra() -> bool {
    false
}

/// Env var from `.cargo/config.toml` `[env]` and from Cargo config.
pub fn env_value() -> &'static str {
    option_env!("CARGO_BUILD_MODEL_ENV").unwrap_or("missing")
}
