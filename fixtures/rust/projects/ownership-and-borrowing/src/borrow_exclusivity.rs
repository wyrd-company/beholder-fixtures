//! RS-CAN-OWN-002: Borrow exclusivity and reborrowing.

/// Accepted non-overlapping reborrows: shorten a mutable borrow via reborrow.
pub fn nonoverlapping_reborrows() -> i32 {
    let mut value = 10;
    let r1 = &mut value;
    {
        let r2: &mut i32 = &mut *r1;
        *r2 += 5;
    }
    // `r2` ended, `r1` still live.
    *r1 += 2;
    value
}

/// Mutable-to-shared reborrow: `&mut T` reborrowed as `&T`.
pub fn mutable_to_shared_reborrow() -> i32 {
    let mut value = 20;
    let m = &mut value;
    let s: &i32 = &*m;
    let copied = *s;
    // Shared reborrow ends; mutable borrow can resume.
    *m += 1;
    copied
}

/// Mutation after last shared use: shared borrow ends at last use, then mutation allowed.
pub fn mutation_after_last_shared_use() -> Vec<i32> {
    let mut data = vec![1, 2, 3];
    let shared = &data;
    let len = shared.len();
    // `shared` last used above; mutation now allowed.
    data.push(len as i32);
    data
}

/// Deref and index places as borrow roots.
pub fn deref_index_places() -> i32 {
    let mut arr = [10, 20, 30];
    let r = &mut arr;
    // Index place through mutable borrow.
    r[1] = 25;
    // Deref place (slice) index.
    let slice: &mut [i32] = &mut *r;
    slice[0] += 1;
    arr[0] + arr[1] + arr[2]
}

/// Borrow across closure boundary: closure borrows shared, then mutation after closure ends.
pub fn borrow_across_closure() -> i32 {
    let mut value = 5;
    {
        let closure = || value + 1;
        let _ = closure();
        // Shared borrow inside closure ended with closure call.
    }
    value += 1;
    value
}

/// Raw-pointer aliasing compiles but may be undefined if misused; valid
/// construction is shown without creating undefined behavior.
/// The invalid simultaneous mutable borrow counterexample is documented in
/// `docs/counterexamples.md` and not present as source.
pub fn raw_pointer_valid_construction() -> i32 {
    let mut value = 42;
    let ptr: *mut i32 = &mut value as *mut i32;
    // Safe to create raw pointer; dereference requires unsafe and must respect aliasing.
    unsafe { *ptr += 1 };
    value
}

pub fn borrow_exclusivity_summary() -> (i32, i32, Vec<i32>) {
    let a = nonoverlapping_reborrows();
    let b = mutable_to_shared_reborrow();
    let c = mutation_after_last_shared_use();
    let _ = deref_index_places();
    let _ = borrow_across_closure();
    let _ = raw_pointer_valid_construction();
    (a, b, c)
}
