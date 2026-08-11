//! RS-CAN-TRAIT-007 — ambiguity and fully qualified syntax.

pub mod alpha {
    /// Trait defining ambiguous items.
    pub trait Alpha {
        fn action(&self) -> &'static str;
        const VALUE: i32;
        type Output;
        fn make() -> Self::Output;
    }
}

pub mod beta {
    /// Second trait with same-named items.
    pub trait Beta {
        fn action(&self) -> &'static str;
        const VALUE: i32;
        type Output;
        fn make() -> Self::Output;
    }
}

pub use alpha::Alpha;
pub use beta::Beta;

pub struct Resolver(pub i32);

impl Alpha for Resolver {
    fn action(&self) -> &'static str {
        "alpha"
    }
    const VALUE: i32 = 10;
    type Output = i32;
    fn make() -> Self::Output {
        10
    }
}

impl Beta for Resolver {
    fn action(&self) -> &'static str {
        "beta"
    }
    const VALUE: i32 = 20;
    type Output = String;
    fn make() -> Self::Output {
        "beta".to_owned()
    }
}

pub fn ambiguity_summary() -> (String, String, String, String, i32, i32, i32, String) {
    let r = Resolver(1);
    // Ambiguity introduced only by importing both traits:
    // `r.action()` would be ambiguous because both `Alpha::action` and
    // `Beta::action` are in scope. The call is preserved as a counterexample
    // in comments and resolved below with both qualification forms.

    // ```rust,ignore
    // let _ambiguous = r.action(); // error: multiple applicable items in scope
    // ```

    let via_alpha_trait = Alpha::action(&r).to_owned();
    let via_alpha_fqs = <Resolver as Alpha>::action(&r).to_owned();
    let via_beta_trait = Beta::action(&r).to_owned();
    let via_beta_fqs = <Resolver as Beta>::action(&r).to_owned();

    // Fully qualified syntax for constants — both `Trait::CONST` and `<Type as Trait>::CONST`.
    let alpha_const_trait = <Resolver as Alpha>::VALUE;
    let beta_const = <Resolver as Beta>::VALUE;

    // Fully qualified syntax for associated types and functions.
    let alpha_made_trait: <Resolver as Alpha>::Output = <Resolver as Alpha>::make();
    let alpha_made_fqs: <Resolver as Alpha>::Output = <Resolver as Alpha>::make();
    let beta_made: <Resolver as Beta>::Output = <Resolver as Beta>::make();
    let beta_made_fqs: <Resolver as Beta>::Output = <Resolver as Beta>::make();
    let _ = (alpha_made_trait, alpha_made_fqs, beta_made_fqs);

    (
        via_alpha_trait,
        via_alpha_fqs,
        via_beta_trait,
        via_beta_fqs,
        alpha_const_trait,
        beta_const,
        alpha_made_trait,
        beta_made,
    )
}

/// Demonstrates `<Type as Trait>::method` versus `Trait::method`.
pub fn fqs_variants(r: &Resolver) -> (&'static str, &'static str, &'static str, &'static str) {
    let a_trait = Alpha::action(r);
    let a_fqs = <Resolver as Alpha>::action(r);
    let b_trait = Beta::action(r);
    let b_fqs = <Resolver as Beta>::action(r);
    (a_trait, a_fqs, b_trait, b_fqs)
}
