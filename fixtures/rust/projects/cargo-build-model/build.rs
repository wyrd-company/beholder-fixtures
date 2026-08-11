fn main() {
    // RS-CAN-PROJ-005: host/target universes, build-script host/target reporting.
    // Emits host and target facts via cargo warnings.
    println!("cargo::rustc-check-cfg=cfg(cargo_config_flag)");
    println!("cargo::rustc-check-cfg=cfg(target_config_flag)");
    println!("cargo::rustc-check-cfg=cfg(extra_flag)");
    println!("cargo::rustc-check-cfg=cfg(doc)");
    println!("cargo::rustc-check-cfg=cfg(doctest)");
    let host = std::env::var("HOST").unwrap_or_else(|_| "unknown-host".to_string());
    let target = std::env::var("TARGET").unwrap_or_else(|_| "unknown-target".to_string());
    println!("cargo:warning=host={} target={}", host, target);

    // RS-CAN-PROJ-005 / RS-CAN-PROJ-022: this build script is itself compiled for
    // the host and links `normal-dep`'s host-role instance (`features =
    // ["host-only"]`), compiled separately from the target-role instance the
    // library links. `role()` returns "host" here.
    println!(
        "cargo:warning=build-script normal-dep role={}",
        normal_dep::role()
    );

    // RS-CAN-PROJ-015: forward real per-profile facts a running binary cannot
    // otherwise observe (Cargo does not expose codegen-units to source code).
    let opt_level = std::env::var("OPT_LEVEL").unwrap_or_else(|_| "unknown".to_string());
    println!("cargo:rustc-env=CARGO_BUILD_MODEL_OPT_LEVEL={}", opt_level);

    println!("cargo:rerun-if-changed=build.rs");
}
