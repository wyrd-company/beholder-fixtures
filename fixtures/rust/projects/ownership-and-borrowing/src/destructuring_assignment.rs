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
///
/// Both wrappers store an ownership-opaque raw pointer (`*mut T` / `*const T`)
/// combined with `PhantomData` and a `Drop` impl to express ownership and
/// drop-check relationships as a combined code-graph signal. The raw pointer
/// alone is opaque; `PhantomData` and `Drop` together complete the
/// ownership/drop-check relationships demonstrated. The fixture is sufficient
/// for code-graph coverage and does not isolate `PhantomData` as the sole
/// cause of the compiler lifetime constraint (see Bob determination).

/// Owning wrapper: owns a heap-allocated `T` reached through an ownership-
/// opaque raw pointer combined with `PhantomData<T>` and a `Drop` that frees
/// the allocation. Together the raw pointer, phantom, and `Drop` express an
/// owning relationship for drop-check and outlives reasoning; the `Drop` that
/// reclaims the allocation makes the ownership claim real.
pub struct Owning<T> {
    ptr: *mut T,
    _owns: PhantomData<T>,
}

impl<T> Owning<T> {
    pub fn new(value: T) -> Self {
        Self {
            ptr: Box::into_raw(Box::new(value)),
            _owns: PhantomData,
        }
    }
    pub fn get(&self) -> &T {
        // Safe: `ptr` came from `Box::into_raw` and is freed only in `Drop`.
        unsafe { &*self.ptr }
    }
}

impl<T> Drop for Owning<T> {
    fn drop(&mut self) {
        // Reconstitute the `Box` to drop the owned `T` and free the allocation.
        unsafe { drop(Box::from_raw(self.ptr)) };
    }
}

/// Non-owning wrapper: refers to a `T` it does not own through the same kind
/// of ownership-opaque raw pointer combined with `PhantomData<&'a T>` and a
/// trivial `Drop`. Together the raw pointer, phantom borrow, and `Drop`
/// express a borrowing relationship that imposes `T: 'a` and shared-borrow
/// variance without claiming ownership or freeing the allocation.
pub struct NonOwning<'a, T> {
    ptr: *const T,
    _borrows: PhantomData<&'a T>,
}

impl<'a, T> NonOwning<'a, T> {
    pub fn new(value: &'a T) -> Self {
        Self {
            ptr: value as *const T,
            _borrows: PhantomData,
        }
    }
    pub fn get(&self) -> &T {
        // Safe: `ptr` derives from a live `&'a T` and `'a` outlives `self`.
        unsafe { &*self.ptr }
    }
}

impl<'a, T> Drop for NonOwning<'a, T> {
    fn drop(&mut self) {}
}

/// Instantiate the combined ownership/drop-check contrast on a lifetime-
/// bearing type. The `Observer` borrows `subject` and reads it during its own
/// `Drop`; `Owning<Observer>` (raw `*mut T` + `PhantomData<T>` + freeing `Drop`)
/// together express ownership that forces drop-check to require `subject` to
/// strictly outlive the wrapper, while `NonOwning` (raw `*const T` +
/// `PhantomData<&'a T>` + `Drop`) borrows and imposes no such owning
/// obligation. The declaration order below satisfies the combined
/// relationship; the reversed order is rejected (E0597, see
/// `docs/counterexamples.md`). The fixture demonstrates the combined
/// raw-pointer/PhantomData/Drop graph relationships, not `PhantomData` in
/// isolation.
pub fn owning_vs_nonowning() -> usize {
    struct Observer<'a>(&'a str);
    impl<'a> Drop for Observer<'a> {
        fn drop(&mut self) {
            // Reads borrowed data during drop; requires it to still be live.
            let _ = self.0.len();
        }
    }

    let subject = String::from("inspected");
    let owning = Owning::new(Observer(&subject));

    let other = String::from("referenced");
    let non_owning = NonOwning::new(&other);

    owning.get().0.len() + non_owning.get().len()
}

pub fn destructuring_assignment_summary() -> (String, u32, i32, String, usize, i32, i32) {
    let (s, n, arr, kept) = nested_destructuring_assignment();
    let a = let_only_pattern();
    let b = evaluation_drop_order();
    let c = owning_vs_nonowning() as i32;
    (s, n, b, kept, a, c, arr)
}
