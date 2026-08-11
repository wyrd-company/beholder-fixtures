//! RS-CAN-MAC-007: procedural spans and hygiene.

// Demonstrate span-carrying generated identifiers and caller resolution distinction
// without depending on diagnostic coordinates.

// Call-site span: identifier resolves as if written at call site
pub fn call_site_demo() -> u32 {
    let call_site_value = 10u32;
    // macro expands to `call_site_value` with Span::call_site(), resolving to above binding
    let resolved = macro_host::call_site_ident!();
    resolved + 5 // 10 + 5 = 15
}

// Mixed-site span: hygienic define does not collide with caller binding
pub fn mixed_site_demo() -> u32 {
    let mixed_site_value = 20u32;
    // hygienic_define generates `let __hygienic_generated = 1u32;` with mixed_site hygiene
    macro_host::hygienic_define!();
    // Caller defines same name but hygienic distinction prevents collision (both coexist via hygiene)
    // Use caller binding plus generated binding (generated is hygienic, caller shadows but both valid)
    let __hygienic_generated = 2u32;
    mixed_site_value + __hygienic_generated
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
    call_site_demo() + mixed_site_demo()
}
