//! `name.rs` file mapping form - standalone file `standalone_file.rs`.

pub fn standalone_fn() -> u32 {
    10
}

pub struct StandaloneType {
    pub v: u32,
}

// Child-directory mapping: `standalone_file/inner_child.rs` is resolved as child of this module.
pub mod inner_child;

pub mod from_inline_child {
    pub fn inner() -> u32 {
        11
    }
}
