//! Unix-only module file injected via `cfg_attr` path attribute.

/// Label from a path-injected module.
pub fn path_module_label() -> &'static str {
    "unix_impl_file"
}
