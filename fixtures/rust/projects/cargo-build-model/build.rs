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
    println!("cargo:rerun-if-changed=build.rs");
}
