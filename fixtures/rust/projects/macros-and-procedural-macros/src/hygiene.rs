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

// Reference invocation-site item via explicit metavar (caller provides identifier)
macro_rules! reference_caller {
    ($var:ident) => {
        $var + 10
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
    let caller_item = 5u32;
    reference_caller!(caller_item)
}

pub fn crate_helper_demo() -> u32 {
    crate_helper_call!()
}

pub fn crate_const_demo() -> u32 {
    crate_const_call!()
}

// Downstream re-export usage: $crate still resolves to defining crate
pub mod downstream {
    pub fn via_downstream() -> u32 {
        crate::crate_helper_call!()
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
        + provider_hygiene_demo()
}
