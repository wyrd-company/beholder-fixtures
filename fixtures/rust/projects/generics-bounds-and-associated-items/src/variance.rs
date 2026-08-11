use std::cell::{Cell, UnsafeCell};
use std::marker::PhantomData;

// RS-CAN-GEN-007: covariance, contravariance, invariance,
// and multiple PhantomData forms with accepted/rejected substitutions.

// Covariant: &'a T is covariant in both 'a and T.
pub fn covariant_substitution<'a, 'b>(value: &'a str) -> &'b str
where
    'a: 'b,
{
    // 'a outlives 'b, so &'a str can be used where &'b str is expected.
    value
}

// Contravariant: fn(T) is contravariant in T.
pub fn contravariant_demo() {
    fn takes_static(_: fn(&'static str)) {}
    fn handler(_: &str) {}
    // fn(&'static str) is subtype of fn(&str) contravariantly, so function
    // expecting fn(&str) can accept fn(&'static str) is not correct direction;
    // correct is opposite. Demonstrate valid assignment:
    let _f: fn(&'static str) = handler;
    takes_static(handler);
}

// Invariant: &mut T and Cell<T> are invariant in T.
pub fn invariant_demo<'a, 'b>(cell: Cell<&'a str>) -> Cell<&'b str>
where
    'a: 'b,
    // This would require invariance violation, documented as counterexample;
    // we demonstrate the invariant form without illegal substitution.
{
    // Cannot coerce Cell<&'a str> to Cell<&'b str> because Cell is invariant.
    // Instead show that we create a new cell.
    let value: &'b str = cell.get();
    Cell::new(value)
}

// PhantomData forms demonstrating variance, ownership, and auto-trait effects.

/// Owned: PhantomData<T> is covariant and drop-check owning.
#[derive(Debug)]
pub struct Owned<T> {
    _marker: PhantomData<T>,
}

/// Non-owning shared: PhantomData<&'a T> is covariant and non-owning.
#[derive(Debug)]
pub struct Shared<'a, T: ?Sized> {
    _marker: PhantomData<&'a T>,
}

/// Mutable invariant: PhantomData<&'a mut T> is invariant over 'a and T.
#[derive(Debug)]
pub struct Mutable<'a, T> {
    _marker: PhantomData<&'a mut T>,
}

/// Function contravariant: PhantomData<fn(T)> is contravariant in T.
#[derive(Debug)]
pub struct Contravariant<T> {
    _marker: PhantomData<fn(T)>,
}

/// Raw const pointer: PhantomData<*const T> is covariant but !Send/? etc. effects.
#[derive(Debug)]
pub struct RawConst<T: ?Sized> {
    _marker: PhantomData<*const T>,
}

/// Raw mut pointer: PhantomData<*mut T> invariant over T, affects auto traits.
#[derive(Debug)]
pub struct RawMut<T> {
    _marker: PhantomData<*mut T>,
}

/// Invariant interior: PhantomData<Cell<T>> invariant.
#[derive(Debug)]
pub struct InvariantCell<T> {
    _marker: PhantomData<Cell<T>>,
}

/// UnsafeCell invariant variant.
#[derive(Debug)]
pub struct InvariantUnsafe<T> {
    _marker: PhantomData<UnsafeCell<T>>,
}

// Variance via interior mutability demonstration.
pub fn variance_with_interior() {
    let _owned: Owned<String> = Owned {
        _marker: PhantomData,
    };
    let _shared: Shared<'static, String> = Shared {
        _marker: PhantomData,
    };
    let _mut_ref: Mutable<'static, String> = Mutable {
        _marker: PhantomData,
    };
    let _contra: Contravariant<String> = Contravariant {
        _marker: PhantomData,
    };
    let _raw_const: RawConst<String> = RawConst {
        _marker: PhantomData,
    };
    let _raw_mut: RawMut<String> = RawMut {
        _marker: PhantomData,
    };
    let _cell: InvariantCell<String> = InvariantCell {
        _marker: PhantomData,
    };
    let _unsafe_cell: InvariantUnsafe<String> = InvariantUnsafe {
        _marker: PhantomData,
    };
}

// Accepted lifetime substitution via covariance.
pub fn accepted_substitution<'short, 'long>(value: Shared<'long, str>) -> Shared<'short, str>
where
    'long: 'short,
{
    // Shared is covariant in 'a, so &'long can substitute for &'short.
    value
}

// Demonstrates that raw pointer PhantomData allows covariance acceptance.
pub fn raw_const_accept<'a, 'b>(value: RawConst<&'a str>) -> RawConst<&'b str>
where
    'a: 'b,
{
    value
}

// Demonstrates invariance: function signature would not allow substitution
// and is preserved as documentation in docs/counterexamples.md.

pub fn phantom_summary() -> &'static str {
    "variance"
}
