//! RS-CAN-TRAIT-002 — coherence, orphan coverage, and overlap.

/// Local trait that can be implemented for foreign types.
pub trait LocalTrait {
    fn local_name(&self) -> &'static str;
}

/// Local nominal type.
pub struct LocalType(pub i32);

/// Newtype workaround for foreign trait on foreign type.
pub struct Wrapper(pub Vec<i32>);

/// Local trait for foreign type (allowed: trait is local).
impl LocalTrait for String {
    fn local_name(&self) -> &'static str {
        "String via LocalTrait"
    }
}

/// Foreign trait for local type (allowed: type is local).
impl std::fmt::Display for LocalType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "LocalType({})", self.0)
    }
}

/// Foreign trait for local wrapper (allowed).
impl std::fmt::Display for Wrapper {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Wrapper({:?})", self.0)
    }
}

/// Local trait for local type (trivial valid impl).
impl LocalTrait for LocalType {
    fn local_name(&self) -> &'static str {
        "LocalType via LocalTrait"
    }
}

/// Covered generic wrapper: local type appears inside Vec.
impl LocalTrait for Vec<LocalType> {
    fn local_name(&self) -> &'static str {
        "Vec<LocalType> via LocalTrait"
    }
}

/// Fundamental inner type with no `Display` or `Debug` impl, so the blanket
/// `impl<T: Display> Display for Box<T>` does not apply.
pub struct FundamentalInner(pub i32);

/// Fundamental-type coverage: `Box<FundamentalInner>` is a fundamental type
/// containing a local type, so a foreign trait impl is legal due to
/// fundamental coverage despite `Box` being foreign and `FundamentalInner`
/// being the first and only generic parameter.
impl std::fmt::Display for Box<FundamentalInner> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "BoxFundamental({})", self.0)
    }
}

/// Second fundamental example: `Box<Wrapper>` uses `Debug` rather than
/// `Display` to avoid conflicting with the blanket `Display for Box<T> where T: Display`
/// (since `Wrapper` already implements `Display`). `Wrapper` does not implement `Debug`,
/// so `Box<Wrapper>: Debug` has no blanket.
impl std::fmt::Debug for Box<Wrapper> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "BoxWrapper({:?})", self.0)
    }
}

/// Fundamental `Box` coverage (second trait): `Box<T>` is `#[fundamental]`, so
/// its single argument `FundamentalInner` (local) is covered and the foreign
/// `Debug` impl is legal. `Box<T>` has one type argument, so this demonstrates
/// fundamental coverage, not parameter order; the ordering cases below use a
/// trait with an additional uncovered type parameter.
impl std::fmt::Debug for Box<FundamentalInner> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "BoxFundamentalDebug({})", self.0)
    }
}

/// Fundamental reference coverage: `&T` is `#[fundamental]` exactly like
/// `Box<T>`, so a foreign trait (`std::ops::Neg`) may be implemented for
/// `&LocalType` because the referent `LocalType` is local. No blanket `Neg`
/// impl exists for references, so this does not conflict.
impl std::ops::Neg for &LocalType {
    type Output = LocalType;
    fn neg(self) -> LocalType {
        LocalType(-self.0)
    }
}

/// Generic uncovered-parameter order: `std::ops::Add<Rhs>` carries an extra type
/// parameter `Rhs`. This impl is legal because the local `LocalType` is the
/// `Self` type and therefore precedes the uncovered, fully generic `Rhs` in the
/// orphan parameter order. Swapping the order to `impl<T> Add<LocalType> for T`
/// would be rejected, since the uncovered `T` (`Self`) would precede the local
/// type. See `docs/counterexamples.md`.
impl<Rhs> std::ops::Add<Rhs> for LocalType {
    type Output = LocalType;
    fn add(self, _rhs: Rhs) -> LocalType {
        LocalType(self.0)
    }
}

pub fn coherence_summary() -> Vec<&'static str> {
    let s = String::from("hello");
    let lt = LocalType(1);
    let lt_ref: &LocalType = &lt;
    vec![
        s.local_name(),
        lt_ref.local_name(),
        LocalType(3).local_name(),
        Vec::<LocalType>::new().local_name(),
    ]
}

pub fn display_summary() -> String {
    let boxed_display = format!("{}", Box::new(FundamentalInner(10)));
    let wrapper_display = format!("{}", Wrapper(vec![1, 2]));
    let boxed_debug = format!("{:?}", Box::new(FundamentalInner(11)));
    format!("{boxed_display} and {wrapper_display} / {boxed_debug}")
}

pub fn fundamental_summary() -> String {
    let a = format!("{}", Box::new(FundamentalInner(20)));
    let b = format!("{:?}", Box::new(FundamentalInner(21)));
    let c = format!("{:?}", Box::new(Wrapper(vec![3, 4])));
    format!("{a}|{b}|{c}")
}

/// Exercises the fundamental-reference impl (`Neg for &LocalType`) and the
/// generic uncovered-parameter-order impl (`Add<Rhs> for LocalType`).
pub fn orphan_order_summary() -> String {
    let negated = -&LocalType(5);
    // `Rhs` is inferred independently at each call: `i32` then `&str`.
    let added_int = LocalType(1) + 99;
    let added_str = LocalType(2) + "ignored";
    format!("{negated}|{added_int}|{added_str}")
}
