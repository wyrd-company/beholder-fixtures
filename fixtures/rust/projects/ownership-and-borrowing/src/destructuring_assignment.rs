//! RS-CAN-OWN-010: Destructuring assignment and drop check.

use std::marker::PhantomData;

pub struct Pair {
    pub first: String,
    pub second: u32,
}

/// Nested tuple/struct/array/slice destructuring assignment.
/// Assignment writes existing places rather than binding new names.
pub fn nested_destructuring_assignment() -> (String, u32, i32, String) {
    let mut s1 = String::new();
    let mut n1: u32 = 0;
    let mut arr_elem: i32 = 0;
    let slice_elem = String::from("slice-elem");

    // Tuple assignment
    let mut a: i32 = 0;
    let mut b: i32 = 0;
    (a, b) = (10, 20);

    // Struct assignment
    let mut pair = Pair {
        first: String::from("init"),
        second: 0,
    };
    Pair {
        first: s1,
        second: n1,
    } = Pair {
        first: String::from("assigned"),
        second: 42,
    };
    // Also nested via tuple containing struct
    let mut nested_first = String::new();
    let mut nested_second: u32 = 0;
    (
        Pair {
            first: nested_first,
            second: nested_second,
        },
        arr_elem,
    ) = (
        Pair {
            first: String::from("nested"),
            second: 99,
        },
        7,
    );

    // Array destructuring assignment
    let mut x: i32 = 0;
    let mut y: i32 = 0;
    let mut z: i32 = 0;
    [x, y, z] = [1, 2, 3];

    // Slice destructuring assignment: clone into existing places
    let mut p = String::from("p");
    let mut q = String::from("q");
    let source = [String::from("alpha"), String::from("beta")];
    [p, q] = source.clone();

    // `_` and field shorthand behavior: `_` discards
    let mut keep = String::from("keep");
    let discard_target = String::from("discard");
    (_, keep) = (String::from("ignored"), String::from("kept"));

    let _ = (
        a,
        b,
        x,
        y,
        z,
        p.clone(),
        q.clone(),
        discard_target.clone(),
        slice_elem.clone(),
        s1.clone(),
        n1,
        arr_elem,
        nested_first.clone(),
        nested_second,
    );
    let _ = pair.second;
    let pair_first = pair.first.clone();
    let pair_second = pair.second;
    // Return representative values without moving `keep` twice.
    (pair_first, pair_second, arr_elem, keep)
}

/// Pattern legal only in `let`, not in destructuring assignment.
/// `ref` bindings and type ascriptions with `:` are valid in `let` patterns
/// but not as assignment targets. We demonstrate the valid `let` form
/// and note the assignment restriction in `docs/counterexamples.md`.
pub fn let_only_pattern() -> usize {
    // Legal in `let`: `ref` binding, `mut` binding with type.
    let ref value = String::from("let-ref");
    let len = value.len();
    let (mut owned, _): (String, i32) = (String::from("typed"), 1);
    owned.push_str("!");
    len + owned.len()
}

/// Evaluation and drop order in destructuring assignment.
pub fn evaluation_drop_order() -> i32 {
    let mut a = 1;
    let mut b = 2;
    // Left-to-right evaluation of assignee expressions, then drop of overwritten values.
    (a, b) = (b, a + b);
    a + b
}

/// Generic wrappers with and without suitable phantom ownership under `Drop`.

/// Owning wrapper: stores `T` by value and carries `PhantomData<T>` to
/// indicate logical ownership. With a `Drop` impl the compiler's drop check
/// requires `T` to strictly outlive the wrapper.
pub struct Owning<T> {
    value: T,
    _marker: PhantomData<T>,
}

impl<T> Owning<T> {
    pub fn new(value: T) -> Self {
        Self {
            value,
            _marker: PhantomData,
        }
    }
    pub fn get(&self) -> &T {
        &self.value
    }
}

impl<T> Drop for Owning<T> {
    fn drop(&mut self) {}
}

/// Non-owning wrapper: borrows `T` and carries `PhantomData<&'a T>` to
/// indicate it does not own `T`. With a `Drop` impl the drop check is more
/// permissive and does not require `T` to outlive the wrapper beyond the
/// borrow.
pub struct NonOwning<'a, T> {
    reference: &'a T,
    _marker: PhantomData<&'a T>,
}

impl<'a, T> NonOwning<'a, T> {
    pub fn new(value: &'a T) -> Self {
        Self {
            reference: value,
            _marker: PhantomData,
        }
    }
    pub fn get(&self) -> &T {
        self.reference
    }
}

impl<'a, T> Drop for NonOwning<'a, T> {
    fn drop(&mut self) {}
}

/// Borrow rejected by destruction order is documented as counterexample in
/// `docs/counterexamples.md`. Valid contrast: `Owning<T>` logically owns `T`
/// (`PhantomData<T>` + `Drop`) and its `T` must outlive the wrapper, while
/// `NonOwning<'a, T>` only borrows (`PhantomData<&'a T>` + `Drop`).

pub fn owning_vs_nonowning() -> i32 {
    let value = 42;
    let owning = Owning::new(value);
    let borrowed = 42;
    let non_owning = NonOwning::new(&borrowed);
    let _ = owning.get();
    let _ = non_owning.get();
    value
}

pub fn destructuring_assignment_summary() -> (String, u32, i32, String, usize, i32, i32) {
    let (s, n, arr, kept) = nested_destructuring_assignment();
    let a = let_only_pattern();
    let b = evaluation_drop_order();
    let c = owning_vs_nonowning();
    (s, n, b, kept, a, c, arr)
}
