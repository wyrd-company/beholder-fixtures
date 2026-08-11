//! RS-CAN-MAC-007: procedural spans and hygiene.

pub const MIXED_SITE_OUTER_VALUE: u32 = 200;

// Call-site span: `call_site_value` with Span::call_site() resolves to caller's local binding
pub fn call_site_demo() -> u32 {
    let call_site_value = 10u32;
    let resolved = macro_host::call_site_ident!();
    resolved + 5
}

// Mixed-site span: `MIXED_SITE_OUTER_VALUE` with Span::mixed_site() resolves to outer item (200)
pub fn mixed_site_demo() -> u32 {
    let via_mixed = macro_host::mixed_site_ident!();
    macro_host::hygienic_define!();
    let __hygienic_generated = 2u32;
    via_mixed + __hygienic_generated
}

// Hygienic define: `__hygienic_generated` with Span::mixed_site() is hygienic, caller binding distinct
pub fn hygienic_binding_demo() -> u32 {
    macro_host::hygienic_define!();
    let __hygienic_generated = 10u32;
    __hygienic_generated + 1
}

// Demonstrate that absolute paths with call_site still resolve correctly downstream
pub mod downstream {
    pub const DOWNSTREAM_CONST: u32 = 30;
    pub fn downstream_helper() -> u32 {
        30
    }
}

// Span choice distinction: call_site vs mixed_site behavior is not tested via diagnostics
// but via value observation that both resolve to caller-provided binding
// Counterexample: generating duplicate identifier with call_site would collide (documented)

pub fn spans_summary() -> u32 {
    call_site_demo() + mixed_site_demo() + hygienic_binding_demo()
}
