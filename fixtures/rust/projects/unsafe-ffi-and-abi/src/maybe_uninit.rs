//! RS-CAN-UNSAFE-002 — staged initialization with `MaybeUninit`.

use core::mem::MaybeUninit;

/// Record constructed via staged field initialization.
#[derive(Debug, PartialEq)]
pub struct Record {
    pub id: u32,
    pub label: String,
    pub flag: bool,
}

/// Staged value initialization with a single `assume_init` after all fields
/// are proven initialized. Validity frontier: `String` and `u32`/`bool` have
/// no invalid bit patterns beyond their type invariants, so `assume_init` is
/// justified only after the staged writes.
pub fn staged_value() -> Record {
    let mut slot: MaybeUninit<Record> = MaybeUninit::uninit();
    let ptr = slot.as_mut_ptr();

    // SAFETY: write each field through the raw pointer; the allocation is valid
    // for the whole `Record` layout and no field is read before being written.
    unsafe {
        core::ptr::addr_of_mut!((*ptr).id).write(7);
        core::ptr::addr_of_mut!((*ptr).label).write(String::from("staged"));
        core::ptr::addr_of_mut!((*ptr).flag).write(true);
        // SAFETY: all fields have been initialized, so the whole value is valid.
        slot.assume_init()
    }
}

/// Staged array initialization with partial-failure cleanup.
/// If initialization were to panic partway through, already initialized
/// elements are dropped. The happy path writes every element and uses a
/// single justified `assume_init`.
pub fn staged_array() -> [String; 3] {
    // Use `MaybeUninit` array to model staged element initialization.
    let mut array: [MaybeUninit<String>; 3] = [
        MaybeUninit::uninit(),
        MaybeUninit::uninit(),
        MaybeUninit::uninit(),
    ];
    let mut initialized = 0usize;

    // Simulate staging; guard ensures cleanup if a panic were to occur between
    // writes. In the non-panicking fixture path every write succeeds.
    struct Guard<'a> {
        slots: &'a mut [MaybeUninit<String>],
        initialized: &'a mut usize,
    }
    impl Drop for Guard<'_> {
        fn drop(&mut self) {
            // Drop only the prefix that was successfully initialized.
            for slot in &mut self.slots[..*self.initialized] {
                // SAFETY: this prefix was initialized before being recorded.
                unsafe { slot.assume_init_drop() };
            }
        }
    }
    let guard = Guard {
        slots: &mut array,
        initialized: &mut initialized,
    };
    // Each write targets a distinct uninitialized slot; `MaybeUninit::write`
    // is safe and the guard records how many elements were initialized.
    guard.slots[0].write(String::from("alpha"));
    *guard.initialized += 1;
    guard.slots[1].write(String::from("beta"));
    *guard.initialized += 1;
    guard.slots[2].write(String::from("gamma"));
    *guard.initialized += 1;

    // All three elements are now initialized; disarm the guard and assume init.
    core::mem::forget(guard);
    // SAFETY: every element has been written exactly once and no drop has run
    // on the uninitialized tail.
    unsafe { array.map(|slot| slot.assume_init()) }
}

/// Demonstrates that reading uninitialized memory or assuming init before
/// validity is UB and therefore never executed; these cases are documented
/// in `docs/counterexamples.md` rather than executed.
pub fn validity_frontier_note() -> &'static str {
    "assume_init only after documented valid initialization"
}
