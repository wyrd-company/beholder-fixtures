//! RS-CAN-MAC-003: declarative hygiene, mixed-site resolution, and $crate.

pub mod helper {
    pub fn helper_value() -> u32 {
        55
    }
    pub const HELPER_CONST: u32 = 77;
}

// Noncolliding local: macro defines __hygiene_local hygienically not colliding
macro_rules! hygiene_local {
    () => {{
        let __hygiene_local = 1u32;
        __hygiene_local + 1
    }};
}

// Explicit identifier that becomes caller-visible via $var
macro_rules! bind_caller {
    ($var:ident = $val:expr) => {
        let $var = $val;
    };
}

// $crate through downstream re-export
#[macro_export]
macro_rules! crate_helper_call {
    () => {
        $crate::hygiene::helper::helper_value()
    };
}

macro_rules! crate_const_call {
    () => {
        $crate::hygiene::helper::HELPER_CONST
    };
}

// Invocation-site item resolution (item vs local hygiene)
macro_rules! use_invocation_item {
    () => {
        INVOCATION_ITEM + 1
    };
}

pub fn noncolliding_demo() -> u32 {
    let __hygiene_local = 100u32; // caller local with same spelling
    // macro's internal __hygiene_local is hygienic, does not collide
    hygiene_local!() + __hygiene_local
}

pub fn explicit_ident_demo() -> u32 {
    bind_caller!(explicit_var = 42);
    explicit_var
}

pub fn invocation_site_demo() -> u32 {
    const INVOCATION_ITEM: u32 = 5;
    use_invocation_item!()
}

pub fn crate_helper_demo() -> u32 {
    crate_helper_call!()
}

pub fn crate_const_demo() -> u32 {
    crate_const_call!()
}

// Downstream re-export: decl_provider's $crate still points to decl_provider
pub mod downstream {
    pub use decl_provider::crate_helper_macro as reexported_crate_macro;
    pub use decl_provider::hygiene_demo as reexported_hygiene;
    pub fn via_downstream() -> u32 {
        reexported_hygiene!(use_crate_helper)
    }
    pub fn via_downstream_macro() -> u32 {
        reexported_crate_macro!()
    }
}

// Provider hygiene macros via decl_provider
pub fn provider_hygiene_demo() -> u32 {
    decl_provider::hygiene_demo!(local) + decl_provider::hygiene_demo!(use_crate_helper)
}

// Counterexamples documented:
// - private helper failure: `hygiene_demo!(use_crate_helper)` would fail if helper were private
// - `$crate` does not bypass visibility
// - nested expansions retain expansion-context identity despite same spelling

pub fn hygiene_summary() -> u32 {
    noncolliding_demo()
        + explicit_ident_demo()
        + invocation_site_demo()
        + crate_helper_demo()
        + crate_const_demo()
        + downstream::via_downstream()
        + downstream::via_downstream_macro()
        + provider_hygiene_demo()
}
