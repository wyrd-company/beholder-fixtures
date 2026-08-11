use std::fmt::{Debug, Display};

// RS-CAN-GEN-002: inline and where bounds, associated projection bounds,
// implied outlives, and higher-ranked trait bounds.

// Inline bounds.
pub fn inline_bound<T: Clone + Debug>(value: T) -> T {
    let cloned = value.clone();
    let _ = format!("{cloned:?}");
    cloned
}

// Where clause equivalent.
pub fn where_bound<T>(value: T) -> T
where
    T: Clone + Debug,
{
    let cloned = value.clone();
    let _ = format!("{cloned:?}");
    cloned
}

// Mixed inline and where.
pub fn mixed_bounds<T: Clone, U>(a: T, b: U) -> (T, U)
where
    U: Debug + Clone,
{
    (a.clone(), b.clone())
}

// Associated projection bound: T::Assoc must implement Display.
pub trait HasOutput {
    type Output;
    fn output(&self) -> Self::Output;
}

pub fn projection_bound<T>(item: T) -> String
where
    T: HasOutput,
    T::Output: Display,
{
    format!("{}", item.output())
}

// Concrete type for projection bound demonstration.
#[derive(Debug)]
pub struct Number(pub i32);

impl HasOutput for Number {
    type Output = i32;
    fn output(&self) -> Self::Output {
        self.0
    }
}

// ?Sized bound: accepts unsized types via reference.
pub fn maybe_sized<T: Display + ?Sized>(value: &T) -> String {
    format!("{value}")
}

// Implied outlives: &'a T implies T: 'a, used without explicit where T: 'a.
pub struct Holder<'a, T> {
    pub reference: &'a T,
}

impl<'a, T> Holder<'a, T> {
    pub fn get(&self) -> &'a T {
        self.reference
    }

    // This method relies on implied T: 'a, no explicit bound needed.
    pub fn map<U, F>(&self, f: F) -> Holder<'a, U>
    where
        F: FnOnce(&'a T) -> &'a U,
    {
        Holder {
            reference: f(self.reference),
        }
    }
}

// Higher-ranked trait bound: callback valid for every lifetime.
pub fn apply_for_all<F>(callback: F) -> String
where
    F: for<'a> Fn(&'a str) -> &'a str,
{
    let first = callback("hello");
    let second = callback(first);
    second.to_owned()
}

// HRTB on function type alias.
pub type ForAllCallback = for<'a> fn(&'a str) -> &'a str;

pub fn invoke_hrtb(callback: ForAllCallback, input: &str) -> String {
    callback(input).to_owned()
}

// Binder placement: for<'a> on trait bound vs function.
pub fn hrtb_binder_demo<F>(func: F)
where
    F: for<'a> Fn(&'a u32) -> u32,
{
    let _ = func(&42);
}

// Trivial bound definition check: where T: Clone is always satisfied for Clone types.
pub trait Trivial<T: Clone> {
    fn echo(&self, value: T) -> T;
}

impl<T: Clone> Trivial<T> for () {
    fn echo(&self, value: T) -> T {
        value.clone()
    }
}

// Higher-ranked function type with where clause.
pub fn higher_ranked_fn<F>(f: F)
where
    F: for<'a> Fn(&'a String) -> usize,
{
    let owned = String::from("example");
    let _ = f(&owned);
}

/// Demonstrates ?Sized with trait object handling.
pub fn sized_contrast() {
    let sized_val: String = maybe_sized(&String::from("sized"));
    let slice: &str = "slice";
    let unsized_val: String = maybe_sized(slice);
    let _ = (sized_val, unsized_val);
    let _number = projection_bound(Number(7));
    let _ = apply_for_all(|s| s);
    let _ = invoke_hrtb(|s| s, "hrtb");
}

pub fn bounds_summary() -> &'static str {
    "bounds"
}
