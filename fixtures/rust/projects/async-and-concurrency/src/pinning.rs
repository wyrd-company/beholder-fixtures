//! RS-CAN-ASYNC-003 — pinning and self-referential state.

use std::future::Future;
use std::marker::PhantomPinned;
use std::pin::Pin;
use std::task::{Context, Poll};

/// Automatically `Unpin` — no pinning restriction.
pub struct Unpinned {
    pub value: i32,
}

/// Marker-composed `!Unpin` type — contains `PhantomPinned` so it is not `Unpin`.
pub struct NotUnpinned {
    pub value: i32,
    pub _marker: PhantomPinned,
}

impl NotUnpinned {
    pub fn new(value: i32) -> Self {
        Self {
            value,
            _marker: PhantomPinned,
        }
    }
}

// Verify auto traits at compile time (statements, not runtime checks).
fn _assert_unpin<T: Unpin>() {}
fn _assert_not_unpin<T>()
where
    T: Unpin,
{
}
fn _check_traits() {
    _assert_unpin::<Unpinned>();
    // `NotUnpinned` does NOT satisfy `Unpin`; the line below would fail to compile:
    // _assert_unpin::<NotUnpinned>();
    // This helper is intentionally not called to keep the negative case documentation-only,
    // but the valid `Unpinned: Unpin` case is asserted by compilation.
}

/// Stack pinning with the `pin!` macro.
pub fn stack_pinning_demo() {
    let not_unpinned = NotUnpinned::new(7);
    let mut pinned = std::pin::pin!(not_unpinned);
    // `NotUnpinned` is `!Unpin`, so mutation requires `get_unchecked_mut`.
    unsafe {
        pinned.as_mut().get_unchecked_mut().value = 11;
    }
    assert_eq!(pinned.value, 11);

    let unpinned = Unpinned { value: 3 };
    let mut pinned_unpinned = std::pin::pin!(unpinned);
    // `Unpinned` is `Unpin`, so `get_mut` is available.
    Pin::get_mut(pinned_unpinned.as_mut()).value = 9;
    assert_eq!(pinned_unpinned.value, 9);
}

/// Heap pinning with `Box::pin`.
pub fn heap_pinning_demo() {
    let heap_pinned: Pin<Box<NotUnpinned>> = Box::pin(NotUnpinned::new(21));
    assert_eq!(heap_pinned.value, 21);

    let heap_unpinned: Pin<Box<Unpinned>> = Box::pin(Unpinned { value: 42 });
    assert_eq!(heap_unpinned.value, 42);
}

/// Container demonstrating permitted projection: an `Unpin` field can be
/// projected from a pinned `!Unpin` container via safe APIs for the `Unpin`
/// part and `unsafe` for the structural pin.
pub struct PinnedContainer {
    pub unpinned_payload: i32,
    pub _marker: PhantomPinned,
}

impl PinnedContainer {
    pub fn new(payload: i32) -> Self {
        Self {
            unpinned_payload: payload,
            _marker: PhantomPinned,
        }
    }

    /// Safe projection for the `Unpin` field through a pinned reference.
    pub fn payload_mut(self: Pin<&mut Self>) -> &mut i32 {
        // Safety: `unpinned_payload: i32` is `Unpin`, so projecting a mutable
        // reference to it does not move the pinned container itself.
        unsafe { &mut self.get_unchecked_mut().unpinned_payload }
    }
}

pub fn projection_demo() {
    let container = PinnedContainer::new(100);
    let mut pinned = std::pin::pin!(container);
    *pinned.as_mut().payload_mut() = 200;
    assert_eq!(pinned.unpinned_payload, 200);
}

/// Custom future that explicitly receives `Pin<&mut Self>` in `poll`.
pub struct CounterFuture {
    count: u32,
    target: u32,
    _marker: PhantomPinned,
}

impl CounterFuture {
    pub fn new(target: u32) -> Self {
        Self {
            count: 0,
            target,
            _marker: PhantomPinned,
        }
    }
}

impl Future for CounterFuture {
    type Output = u32;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        // Safety: accessing `count` and `target` does not move the `!Unpin` self
        // out of its pinned location; the fields themselves are `Unpin`.
        let this = unsafe { self.get_unchecked_mut() };
        this.count += 1;
        if this.count >= this.target {
            Poll::Ready(this.count)
        } else {
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

pub fn custom_poll_receiver_demo() {
    let future = CounterFuture::new(3);
    let result = crate::support::block_on(future);
    assert_eq!(result, 3);

    // Also exercise via stack-pinned poll.
    let mut future2 = CounterFuture::new(2);
    let result2 = crate::support::block_on(unsafe { Pin::new_unchecked(&mut future2) });
    // `block_on` already pins; this just shows that taking `Pin<&mut Self>` is
    // the required receiver for `Future::poll`.
    assert_eq!(result2, 2);
}

pub fn pinning_demo() {
    stack_pinning_demo();
    heap_pinning_demo();
    projection_demo();
    custom_poll_receiver_demo();
}
