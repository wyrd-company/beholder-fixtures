//! RS-CAN-MAC-008: compiler built-in and contextual macros.

// Demonstrate source location and contextual macros
pub fn location_demo() -> String {
    let file = file!();
    let line = line!();
    let column = column!();
    let path = module_path!();
    format!("{file}:{line}:{column}:{path}")
}

// Environment presence and absence
pub fn env_demo() -> String {
    // Present: CARGO_PKG_NAME is set by Cargo
    let pkg = env!("CARGO_PKG_NAME");
    // Absent: use option_env!
    let absent = option_env!("FIXTURE_ABSENT_ENV_VAR_NOT_SET");
    let absent_str = absent.unwrap_or("missing");
    // Tracked vs untracked env: option_env! is tracked, we just demonstrate presence/absence
    format!("{pkg}:{absent_str}")
}

// Formatting macros
pub fn formatting_demo() -> String {
    let value = 42;
    let formatted = format!("value={value}");
    let args = format_args!("value={}", value);
    format!("{formatted}:{}", args)
}

// cfg! boolean (does not remove code; both branches remain type-checked)
pub fn cfg_demo() -> bool {
    let is_unix = cfg!(unix);
    let _unused = if cfg!(unix) { 1u32 } else { 2u32 };
    is_unix || !is_unix
}

// Inclusion macros
pub fn include_demo() -> &'static str {
    // include_str! includes data at compile time; use known file
    let data = include_str!("../crates/macro_host/data/records.txt");
    // include_bytes! variant
    let bytes = include_bytes!("../crates/macro_host/data/records.txt");
    // Use both to avoid unused
    assert!(!data.is_empty());
    assert!(!bytes.is_empty());
    data.lines().next().unwrap_or("")
}

// Intentional gated error (compile_error! not executed, gated by cfg)
#[cfg(any())]
compile_error!("this cfg-gated compile_error is intentional and never compiled");

// Data/source inclusion and concatenation/stringification
pub fn concat_stringify_demo() -> String {
    let concatted = concat!("hello", "_", "world");
    let stringified = stringify!(hello world 123);
    let sample = 1u32;
    let asserted = {
        assert!(sample == 1);
        assert_eq!(sample, 1);
        "ok"
    };
    let value = Some(5);
    let matched = value.is_some();
    let collection = vec![1, 2, 3];
    format!("{concatted}:{stringified}:{asserted}:{matched}:{collection:?}")
}

// Build-gated inclusion with cfg
#[cfg(unix)]
pub fn platform_gate() -> &'static str {
    "unix"
}

#[cfg(not(unix))]
pub fn platform_gate() -> &'static str {
    "other"
}

pub fn builtins_summary() -> String {
    format!(
        "{}|{}|{}|{}|{}|{}|{}",
        location_demo(),
        env_demo(),
        formatting_demo(),
        cfg_demo(),
        include_demo(),
        concat_stringify_demo(),
        platform_gate()
    )
}
