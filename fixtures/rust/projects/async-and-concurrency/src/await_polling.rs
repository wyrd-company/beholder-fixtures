//! RS-CAN-ASYNC-002 — await, polling, cancellation, and suspension borrows.
#![allow(clippy::ptr_arg, clippy::new_without_default, clippy::drop_non_drop)]

use std::future::{Future, IntoFuture};
use std::pin::Pin;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::task::{Context, Poll};

/// A custom future that returns `Pending` on the first poll and `Ready` thereafter.
pub struct PendingToReady {
    polled: bool,
    value: u32,
}

impl PendingToReady {
    pub fn new(value: u32) -> Self {
        Self {
            polled: false,
            value,
        }
    }
}

impl Future for PendingToReady {
    type Output = u32;

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        if self.polled {
            Poll::Ready(self.value)
        } else {
            self.polled = true;
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

/// Wrapper that implements `IntoFuture` converting via `PendingToReady`.
pub struct IntoFutureWrapper(pub u32);

impl IntoFuture for IntoFutureWrapper {
    type Output = u32;
    type IntoFuture = PendingToReady;

    fn into_future(self) -> Self::IntoFuture {
        PendingToReady::new(self.0)
    }
}

/// Yield-once future used as a suspension point that retains borrows and locals.
pub struct YieldOnce {
    yielded: bool,
}

impl YieldOnce {
    pub fn new() -> Self {
        Self { yielded: false }
    }
}

impl Default for YieldOnce {
    fn default() -> Self {
        Self::new()
    }
}

impl Future for YieldOnce {
    type Output = ();

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        if self.yielded {
            Poll::Ready(())
        } else {
            self.yielded = true;
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

static DROP_COUNT: AtomicUsize = AtomicUsize::new(0);

/// Future whose `Drop` is observable, used to demonstrate cancellation on drop.
pub struct DropOnCancel {
    yielded: bool,
}

impl DropOnCancel {
    pub fn new() -> Self {
        Self { yielded: false }
    }

    pub fn drop_count() -> usize {
        DROP_COUNT.load(Ordering::SeqCst)
    }

    pub fn reset_drop_count() {
        DROP_COUNT.store(0, Ordering::SeqCst);
    }
}

impl Drop for DropOnCancel {
    fn drop(&mut self) {
        DROP_COUNT.fetch_add(1, Ordering::SeqCst);
    }
}

impl Future for DropOnCancel {
    type Output = &'static str;

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        if self.yielded {
            Poll::Ready("completed")
        } else {
            self.yielded = true;
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

/// Await `PendingToReady` and `IntoFutureWrapper`, demonstrating `IntoFuture` conversion.
pub async fn custom_future_await_demo() -> u32 {
    let first = PendingToReady::new(10).await;
    let second = IntoFutureWrapper(32).await;
    first + second
}

/// Hold a shared borrow across a suspension point.
pub async fn borrow_across_suspension(value: &String) -> usize {
    let borrowed: &String = value;
    let len_before = borrowed.len();
    YieldOnce::new().await;
    // `borrowed` is still live across the await.
    len_before + borrowed.len()
}

/// Hold a mutable borrow across suspension and mutate after waking.
pub async fn mutable_borrow_across_suspension(value: &mut Vec<u32>) -> usize {
    let len_before = value.len();
    YieldOnce::new().await;
    value.push(99);
    len_before + value.len()
}

/// Demonstrate dropping a suspended future with observable cleanup.
pub fn drop_suspended_future_demo() {
    use crate::support::poll_once;

    DropOnCancel::reset_drop_count();

    // Pin the future and poll once to `Pending`, then drop without completing.
    let mut future = DropOnCancel::new();
    let poll = {
        let mut pinned = unsafe { Pin::new_unchecked(&mut future) };
        poll_once(pinned.as_mut())
    };
    assert!(poll.is_pending());
    // Dropping `future` here cancels remaining work and runs `Drop`.
    drop(future);
    assert_eq!(DropOnCancel::drop_count(), 1);

    // In contrast, running to completion also drops exactly once but after `Ready`.
    DropOnCancel::reset_drop_count();
    let result = crate::support::block_on(DropOnCancel::new());
    assert_eq!(result, "completed");
    assert_eq!(DropOnCancel::drop_count(), 1);
}

pub fn await_polling_demo() {
    let sum = crate::support::block_on(custom_future_await_demo());
    assert_eq!(sum, 42);

    let owned = String::from("suspension-borrow");
    let len = crate::support::block_on(borrow_across_suspension(&owned));
    assert_eq!(len, owned.len() * 2);

    let mut data = vec![1, 2, 3];
    let before = data.len();
    let after = crate::support::block_on(mutable_borrow_across_suspension(&mut data));
    assert_eq!(after, before + 4);
    assert_eq!(data.len(), 4);

    drop_suspended_future_demo();
}
