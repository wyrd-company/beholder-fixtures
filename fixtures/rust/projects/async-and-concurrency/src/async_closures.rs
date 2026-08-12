//! RS-CAN-ASYNC-004 — async closures and async call traits.
//! Stable from Rust 1.85 (edition 2024).
#![allow(clippy::redundant_closure_call)]

use std::ops::{AsyncFn, AsyncFnMut, AsyncFnOnce};

/// Call an async closure that only reads its captures — bounds as `AsyncFn`.
pub async fn call_reading<F>(f: &F) -> i32
where
    F: AsyncFn() -> i32,
{
    f().await
}

/// Call an async closure that mutates its captures — bounds as `AsyncFnMut`.
pub async fn call_mutating<F>(f: &mut F) -> i32
where
    F: AsyncFnMut() -> i32,
{
    f().await
}

/// Call an async closure that consumes its captures — bounds as `AsyncFnOnce`.
pub async fn call_consuming<F>(f: F) -> String
where
    F: AsyncFnOnce() -> String,
{
    f().await
}

/// Ordinary closure that returns an async block (contrast with an async closure).
pub fn closure_returning_async_block(
    captured: i32,
) -> impl Fn() -> std::pin::Pin<Box<dyn std::future::Future<Output = i32>>> {
    move || Box::pin(async move { captured + 5 })
}

mod future {
    use std::future::Future;
    use std::pin::Pin;
    use std::task::{Context, Poll};

    pub struct ReturnFuture {
        value: i32,
    }

    impl Future for ReturnFuture {
        type Output = i32;

        fn poll(self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<Self::Output> {
            // Simplified: immediately ready without suspension.
            Poll::Ready(unsafe { self.get_unchecked_mut().value })
        }
    }

    impl From<i32> for ReturnFuture {
        fn from(value: i32) -> Self {
            Self { value }
        }
    }
}

pub fn async_closure_demo() {
    // Reading async closure: captures by shared borrow, can be called repeatedly.
    let base = 10;
    let reading = async || base + 5;
    let first = crate::support::block_on(call_reading(&reading));
    let second = crate::support::block_on(call_reading(&reading));
    assert_eq!(first, 15);
    assert_eq!(second, 15);

    // Repeated calls via the same `AsyncFn` value.
    let repeated = async || base * 2;
    let a = crate::support::block_on(call_reading(&repeated));
    let b = crate::support::block_on(call_reading(&repeated));
    assert_eq!(a, 20);
    assert_eq!(b, 20);

    // Mutating async closure: captures by mutable borrow, implements `AsyncFnMut`.
    let mut counter: i32 = 0;
    let mut mutating = async || {
        counter += 1;
        counter
    };
    let m1 = crate::support::block_on(call_mutating(&mut mutating));
    assert_eq!(m1, 1);
    let m2 = crate::support::block_on(call_mutating(&mut mutating));
    assert_eq!(m2, 2);

    // Consuming async closure: `async move` takes ownership, implements `AsyncFnOnce`.
    let owned = String::from("consume-me");
    let consuming = async move || owned;
    let consumed = crate::support::block_on(call_consuming(consuming));
    assert_eq!(consumed, "consume-me");

    // Ordinary closure returning an async block — distinct from an async closure.
    // `|| async { ... }` returns a future on each call; `async || { ... }` is itself async.
    let ordinary = closure_returning_async_block(7);
    let ordinary_result = crate::support::block_on(ordinary());
    assert_eq!(ordinary_result, 12);

    // Named custom future variant preserved (opaque future via ReturnFuture).
    let custom = future::ReturnFuture::from(42);
    let custom_result = crate::support::block_on(custom);
    assert_eq!(custom_result, 42);

    // Direct async closure literals driven without a helper bound.
    // An async closure is not itself a `Future`; it must be called to obtain one.
    let direct = crate::support::block_on((async || 123)());
    assert_eq!(direct, 123);

    let direct_move = crate::support::block_on((async move || {
        let s = String::from("direct");
        s.len() as i32
    })());
    assert_eq!(direct_move, 6);
}
