//! Minimal in-project executor for driving futures without a third-party runtime.

use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll, RawWaker, RawWakerVTable, Waker};

fn noop_clone(_data: *const ()) -> RawWaker {
    noop_raw_waker()
}

fn noop_wake(_data: *const ()) {}

fn noop_wake_by_ref(_data: *const ()) {}

fn noop_drop(_data: *const ()) {}

const NOOP_VTABLE: RawWakerVTable =
    RawWakerVTable::new(noop_clone, noop_wake, noop_wake_by_ref, noop_drop);

fn noop_raw_waker() -> RawWaker {
    RawWaker::new(std::ptr::null(), &NOOP_VTABLE)
}

fn noop_waker() -> Waker {
    unsafe { Waker::from_raw(noop_raw_waker()) }
}

/// Drive a future to completion by polling with a no-op waker.
pub fn block_on<F: Future>(mut future: F) -> F::Output {
    let waker = noop_waker();
    let mut ctx = Context::from_waker(&waker);
    // Safety: pin on stack without moving after first poll.
    let mut pinned = unsafe { Pin::new_unchecked(&mut future) };
    loop {
        match pinned.as_mut().poll(&mut ctx) {
            Poll::Ready(value) => return value,
            Poll::Pending => continue,
        }
    }
}

/// Poll a pinned future once with a no-op waker.
pub fn poll_once<F: Future>(future: Pin<&mut F>) -> Poll<F::Output> {
    let waker = noop_waker();
    let mut ctx = Context::from_waker(&waker);
    future.poll(&mut ctx)
}

/// Consume any future through a generic `Future` bound.
pub async fn consume_future<F>(future: F) -> F::Output
where
    F: Future,
{
    future.await
}

/// Assert that a value is `Send`.
pub fn assert_send<T: Send>(_value: T) {}
