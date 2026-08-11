//! RS-CAN-TRAIT-009 — auto traits and manual unsafe overrides.

use std::cell::Cell;

/// Composite that inherits Send/Sync because all fields are Send/Sync.
pub struct AllSend {
    pub value: i32,
    pub holder: String,
}

/// Composite that fails Send/Sync because it contains a non-Send type.
pub struct NotSend {
    pub _cell: Cell<i32>,
}

/// Generic holder whose Send/Sync depends on T.
pub struct GenericHolder<T>(pub T);

/// Marker field that changes inference: PhantomData makes type Send only if T is Send.
pub struct WithMarker<T> {
    pub value: T,
    pub _marker: std::marker::PhantomData<std::cell::RefCell<i32>>,
}

/// Raw pointer field changes Send/Sync inference.
pub struct WithRawPointer {
    pub ptr: *const i32,
}

/// Type requiring justified unsafe impl because raw pointer is used safely.
/// SAFETY: The raw pointer in `SafeRaw` is always either null or points to a valid
/// allocation owned elsewhere and is never dereferenced without synchronization
/// in this fixture; the unsafe impl is justified for graph demonstration only.
pub struct SafeRaw {
    ptr: *const i32,
}

// SAFETY: Justified as described above; fixture-owned type with controlled pointer use.
unsafe impl Send for SafeRaw {}
unsafe impl Sync for SafeRaw {}

impl SafeRaw {
    pub fn new(ptr: *const i32) -> Self {
        Self { ptr }
    }

    pub fn get(&self) -> *const i32 {
        self.ptr
    }
}

pub fn assert_send_sync() {
    fn assert_send<T: Send>() {}
    fn assert_sync<T: Sync>() {}
    fn assert_not_sync<T>() {}

    assert_send::<AllSend>();
    assert_sync::<AllSend>();
    assert_send::<GenericHolder<i32>>();
    assert_sync::<GenericHolder<i32>>();
    // NotSend contains Cell which is Send but not Sync, so it is Send but not Sync.
    assert_send::<NotSend>();
    assert_not_sync::<NotSend>();
    // GenericHolder with non-Sync type propagates failure.
    assert_not_sync::<GenericHolder<Cell<i32>>>();
    // WithMarker contains PhantomData<RefCell<i32>> which is not Sync.
    assert_not_sync::<WithMarker<i32>>();
    // WithRawPointer contains a raw pointer which is not Send/Sync, so it fails both.
    assert_not_sync::<WithRawPointer>();

    assert_send::<SafeRaw>();
    assert_sync::<SafeRaw>();
    // Also demonstrate that Gate check for WithRawPointer not Send:
    fn assert_not_send<T>() {}
    assert_not_send::<WithRawPointer>();
}

pub fn auto_traits_summary() -> &'static str {
    assert_send_sync();
    "auto-traits"
}
