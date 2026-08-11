use std::env;
use std::fs;
use std::path::PathBuf;

fn main() {
    // RS-CAN-PROJ-011: build-script protocol directives.

    // Rerun triggers: file-based and environment-based.
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-changed=src/lib.rs");
    println!("cargo:rerun-if-changed=src/dual_source.rs");
    println!("cargo:rerun-if-changed=crates/fixture-native-sys/build.rs");
    println!("cargo:rerun-if-env-changed=FIXTURE_RERUN_ENV");
    println!("cargo:rerun-if-env-changed=FIXTURE_CONDITIONAL");
    println!("cargo:rerun-if-env-changed=FIXTURE_GENERATED_SEED");
    println!("cargo:rerun-if-env-changed=DEP_FIXTURE_NATIVE_FIXTURE_KIND");

    // rustc-check-cfg and rustc-cfg: declare and set cfg.
    println!("cargo:rustc-check-cfg=cfg(fixture_build_cfg)");
    println!("cargo:rustc-cfg=fixture_build_cfg");
    println!("cargo:rustc-check-cfg=cfg(host_target_match)");
    println!("cargo:rustc-check-cfg=cfg(fixture_conditional)");

    // rustc-env: expose environment to compiled Rust.
    println!("cargo:rustc-env=FIXTURE_BUILD_ENV=build_env_value");
    // Conditional env derived from host/target probe or DEP metadata.
    if let Ok(kind) = env::var("DEP_FIXTURE_NATIVE_FIXTURE_KIND") {
        println!("cargo:rustc-env=CONSUMED_NATIVE_KIND={kind}");
        println!("cargo:rustc-env=CONSUMED_NATIVE_PRESENT=1");
    } else {
        println!("cargo:rustc-env=CONSUMED_NATIVE_PRESENT=0");
    }

    // Host/target probe and conditional output.
    let host = env::var("HOST").unwrap_or_else(|_| "unknown".to_string());
    let target = env::var("TARGET").unwrap_or_else(|_| "unknown".to_string());
    println!("cargo:rustc-env=FIXTURE_HOST={host}");
    println!("cargo:rustc-env=FIXTURE_TARGET={target}");
    if host == target {
        println!("cargo:rustc-cfg=host_target_match");
    }
    // Conditional output based on environment.
    let conditional = env::var("FIXTURE_CONDITIONAL").unwrap_or_else(|_| "0".to_string());
    if conditional == "1" {
        println!("cargo:rustc-cfg=fixture_conditional");
        println!("cargo:rustc-env=FIXTURE_CONDITIONAL_VALUE=yes");
    } else {
        println!("cargo:rustc-env=FIXTURE_CONDITIONAL_VALUE=no");
    }

    // Link directives: search, library, argument (benign, valid).
    let out_dir = PathBuf::from(env::var("OUT_DIR").expect("OUT_DIR not set"));
    // Search path: OUT_DIR (exists) and a standard system path.
    println!("cargo:rustc-link-search=native={}", out_dir.display());
    println!("cargo:rustc-link-search=native=/usr/lib");
    // Library directive: link to a system library that exists (libm).
    println!("cargo:rustc-link-lib=dylib=m");
    // Argument directive: benign linker argument.
    println!("cargo:rustc-link-arg=-Wl,-z,relro");

    // Metadata directive (non-links propagation, valid for RS-CAN-PROJ-011).
    println!("cargo:fixture_build_meta=build_meta_value");
    println!("cargo:fixture_build_meta_extra=extra_value");

    // Warning directive (Cargo will surface as warning, valid protocol).
    println!("cargo:warning=build script executed for build-scripts-and-codegen");

    // RS-CAN-PROJ-012 + RS-CAN-ECO-004: generate Rust and data into OUT_DIR.
    // Generator source is committed (this build.rs); OUT_DIR output is artifact.

    // Generated Rust items referenced by handwritten code.
    let seed = env::var("FIXTURE_GENERATED_SEED").unwrap_or_else(|_| "42".to_string());
    let generated_items = format!(
        r#"// Generated items for RS-CAN-PROJ-012.
pub struct GeneratedItem {{
    pub value: u32,
}}

pub const GENERATED_CONST: u32 = {seed};

pub fn generated_fn() -> u32 {{
    {seed}
}}

pub const GENERATED_SEED_STR: &str = "{seed}";
"#
    );
    fs::write(out_dir.join("generated_items.rs"), generated_items)
        .expect("write generated_items.rs");

    // Generated expression (to be included as expression).
    let generated_expr = format!("{seed} + 1");
    fs::write(out_dir.join("generated_expression.rs"), generated_expr)
        .expect("write generated_expression.rs");

    // Separate embedded text and bytes.
    fs::write(out_dir.join("generated_text.txt"), "hello fixture\n")
        .expect("write generated_text.txt");
    fs::write(
        out_dir.join("generated_bytes.bin"),
        [0x01u8, 0x02, 0x03, 0xFF],
    )
    .expect("write generated_bytes.bin");

    // File that will be both included and module-mounted (via generated path).
    // This demonstrates distinct entities from same textual source.
    let dual_content = r#"pub struct DualType(pub u32);

impl DualType {
    pub fn value(&self) -> u32 {
        self.0
    }
}

pub const DUAL_CONST: u32 = 99;
"#;
    fs::write(out_dir.join("dual.rs"), dual_content).expect("write dual.rs");

    // Changed generated result without source-tree Rust edit:
    // The value above varies with FIXTURE_GENERATED_SEED env var,
    // so editing the environment changes OUT_DIR output without touching src/.

    // Note: OUT_DIR artifacts are not tracked source; regeneration by `build` is expected.
    // See docs/counterexamples.md for missing output and other counterexamples.
}
