//! RS-CAN-ASYNC-005 — future sendability across suspension.

use std::rc::Rc;

use crate::await_polling::YieldOnce;
use crate::support::{assert_send, block_on};

/// Future that holds a non-`Send` value only *before* its suspension point.
/// Because the `Rc` is dropped at the end of an inner block before `await`,
/// the future itself remains `Send`.
pub async fn sendable_future() -> u32 {
    let value = {
        let rc = Rc::new(7);
        *rc
    };
    YieldOnce::new().await;
    value as u32
}

/// Near-identical future that holds the same non-`Send` value *across* suspension.
/// Retaining `Rc` across `await` makes the future `!Send`.
pub async fn non_sendable_future() -> u32 {
    let rc = Rc::new(7);
    YieldOnce::new().await;
    // `rc` is still live here, so the compiler retains it across the suspension.
    *rc as u32
}

/// Spawn-style API that requires `Send`.
pub fn require_send<F>(future: F) -> F
where
    F: Future + Send,
    F::Output: Send,
{
    future
}

use std::future::Future;

/// Demonstrate that a `Send`-checked API accepts the sendable future
/// and that the non-sendable variant is distinct.
pub fn sendability_demo() {
    // This future is `Send` because the `Rc` does not cross the await.
    let sendable = sendable_future();
    assert_send(sendable);
    let sendable2 = sendable_future();
    let _accepted = require_send(sendable2);

    // The same value held across await makes the future `!Send`.
    // The following would fail to compile if uncommented:
    // let non_sendable = non_sendable_future();
    // assert_send(non_sendable);
    // let non_sendable2 = non_sendable_future();
    // let _rejected = require_send(non_sendable2);

    // Both futures still execute correctly when not `Send`-checked.
    let a = block_on(sendable_future());
    let b = block_on(non_sendable_future());
    assert_eq!(a, 7);
    assert_eq!(b, 7);

    // Explicit scope also controls sendability: inner-block drop before await keeps `Send`.
    let scoped_send = async {
        let v = {
            let rc = Rc::new(42);
            *rc
        };
        YieldOnce::new().await;
        v
    };
    assert_send(scoped_send);

    // The precise body change breaking downstream `Send` is the difference between
    // these two blocks — only the suspension-crossing retention matters.
    let scoped_non_send = async {
        let rc = Rc::new(42);
        YieldOnce::new().await;
        *rc
    };
    // `scoped_non_send` is `!Send`; not passed to `assert_send`/`require_send`.
    let _ = block_on(scoped_non_send);
}
