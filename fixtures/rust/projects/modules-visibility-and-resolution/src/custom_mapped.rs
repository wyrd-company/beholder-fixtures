//! File mounted via `#[path]` attribute.

pub fn custom_fn() -> u32 {
    40
}

// Nested child resolved via default file mapping relative to this file's logical path.
// Since this file is mounted as `custom_mapped`, its child `nested` resolves to `custom_mapped/nested.rs`
// but we demonstrate `#[path]` for nested as well.
#[path = "custom_nested.rs"]
pub mod nested;

pub mod inline_nested_child {
    pub fn value() -> u32 {
        41
    }
}
