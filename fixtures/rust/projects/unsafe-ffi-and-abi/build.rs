fn main() {
    // RS-CAN-FFI-002: native library selection with build-script link directives.
    // Search path and library selection are emitted unconditionally; the chosen
    // library `m` exists on the host `x86_64-unknown-linux-gnu` target and the
    // link succeeds without requiring C compilation.
    println!("cargo:rustc-link-search=native=/usr/lib");
    println!("cargo:rustc-link-lib=dylib=m");
    println!("cargo:rustc-link-arg=-Wl,-z,relro");
    println!("cargo:rustc-check-cfg=cfg(ffi_build_linked)");
    println!("cargo:rustc-cfg=ffi_build_linked");
    println!("cargo:rerun-if-changed=build.rs");
}
