//! RS-CAN-TRAIT-007 — ambiguity and fully qualified syntax.

pub trait Alpha {
    fn action(&self) -> &'static str;
    const VALUE: i32;
    type Output;
    fn make() -> Self::Output;
}

pub trait Beta {
    fn action(&self) -> &'static str;
    const VALUE: i32;
    type Output;
    fn make() -> Self::Output;
}

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

/// Inherent method colliding with trait methods.
impl Resolver {
    pub fn action(&self) -> &'static str {
        "inherent"
    }
}

pub fn ambiguity_summary() -> (String, String, String, i32, i32, i32, String) {
    let r = Resolver(1);
    // Bring both traits into scope to create an ambiguous `action` situation.
    // Direct call `r.action()` would select inherent; trait calls require qualification.
    let inherent = r.action().to_owned();
    let via_alpha = Alpha::action(&r).to_owned();
    let via_beta = Beta::action(&r).to_owned();

    // Fully qualified syntax for constants.
    let alpha_const = <Resolver as Alpha>::VALUE;
    let beta_const = <Resolver as Beta>::VALUE;

    // Fully qualified syntax for associated types and functions.
    let alpha_made: <Resolver as Alpha>::Output = <Resolver as Alpha>::make();
    let beta_made: <Resolver as Beta>::Output = <Resolver as Beta>::make();

    (
        inherent,
        via_alpha,
        via_beta,
        alpha_const,
        beta_const,
        alpha_made,
        beta_made,
    )
}

/// Demonstrates `<Type as Trait>::method` versus `Trait::method`.
pub fn fqs_variants(r: &Resolver) -> (&'static str, &'static str) {
    let a = <Resolver as Alpha>::action(r);
    let b = Beta::action(r);
    (a, b)
}
