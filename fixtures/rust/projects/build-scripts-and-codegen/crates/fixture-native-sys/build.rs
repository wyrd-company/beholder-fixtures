use std::env;
use std::path::Path;

fn main() {
    // RS-CAN-PROJ-020: links ownership already declared in Cargo.toml (`links = "fixture_native"`).
    // Emit build metadata for direct dependents.

    // Rerun triggers for hermetic native input.
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-changed=native/native.c");
    println!("cargo:rerun-if-changed=native/native.h");
    println!("cargo:rerun-if-env-changed=FIXTURE_NATIVE_SEED");

    // Host probe for conditional output (also used in RS-CAN-PROJ-011-style logic).
    let host = env::var("HOST").unwrap_or_else(|_| "unknown-host".to_string());
    let target = env::var("TARGET").unwrap_or_else(|_| "unknown-target".to_string());
    if host == target {
        println!("cargo:rustc-cfg=native_available");
        println!("cargo:rustc-check-cfg=cfg(native_available)");
    }

    // Compile hermetic vendored translation unit via pinned cc.
    let out_dir = env::var("OUT_DIR").expect("OUT_DIR not set");
    cc::Build::new()
        .file(Path::new("native/native.c"))
        .include(Path::new("native"))
        .compile("fixture_native");

    // RS-CAN-PROJ-020: emitted build metadata consumable via DEP_FIXTURE_NATIVE_*.
    println!("cargo:root={out_dir}");
    println!("cargo:include={out_dir}");
    println!("cargo:fixture_kind=native");
    println!("cargo:fixture_version=1");
    // Additional metadata key.
    println!("cargo:native_out_dir={out_dir}");

    // Also emit a benign cfg for downstream visibility check (requires check-cfg).
    println!("cargo:rustc-check-cfg=cfg(fixture_native_cfg)");
    println!("cargo:rustc-cfg=fixture_native_cfg");

    // Note: DEP_* variables are only visible to direct dependent build scripts,
    // not to ordinary crate environment. See docs/counterexamples.md.
}
