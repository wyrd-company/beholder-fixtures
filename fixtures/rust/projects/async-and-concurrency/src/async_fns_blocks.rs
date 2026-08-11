//! RS-CAN-ASYNC-001 — async functions/blocks and opaque futures.

use crate::support::{block_on, consume_future};

// Each async function produces a distinct opaque future state machine.
pub async fn async_add(a: i32, b: i32) -> i32 {
    a + b
}

pub async fn async_greeting(name: String) -> String {
    format!("hello {name}")
}

// Demonstrate that two async functions have distinct anonymous future types.
pub fn distinct_future_types_demo() {
    let fa = async_add(1, 2);
    let fb = async_greeting("world".to_string());
    // `fa` and `fb` have different anonymous types; they are not interchangeable,
    // but both satisfy the same generic Future bound when driven.
    let _ = std::mem::size_of_val(&fa);
    let _ = std::mem::size_of_val(&fb);
}

// Async function with a local that crosses suspension.
pub async fn local_crossing_suspension(input: i32) -> i32 {
    let local = input * 3;
    // Yield once so `local` must be retained across suspension.
    crate::await_polling::YieldOnce::new().await;
    local + 1
}

// Helper awaitable used above and shared with other modules.
pub async fn simple_value() -> u32 {
    42
}

/// Demonstrate non-move and move async blocks with locals crossing suspension.
pub fn async_blocks_demo() {
    let borrowed_value = String::from("borrowed-demo");
    let owned_value = String::from("owned-demo");

    // Non-move async block borrowing from the environment.
    let borrowed_len = borrowed_value.len();
    let non_move_block = async {
        let local = borrowed_len + 10;
        crate::await_polling::YieldOnce::new().await;
        local + borrowed_value.len()
    };

    // Move async block capturing owned data.
    let move_block = async move {
        let local = owned_value.len() + 5;
        crate::await_polling::YieldOnce::new().await;
        local + owned_value.len()
    };

    // Multiple move blocks each capture distinct locals.
    let move_block_a = async move {
        let local_a = 7;
        crate::await_polling::YieldOnce::new().await;
        local_a * 2
    };
    let move_block_b = async move {
        let local_b = 11;
        crate::await_polling::YieldOnce::new().await;
        local_b + 3
    };

    // Futures are not started until polled; construction alone has no effect.
    let _constructed_not_polled = async { 99_u32 };

    // Drive each block through a generic Future bound.
    let _ = block_on(consume_future(non_move_block));
    let _ = block_on(consume_future(move_block));
    let _ = block_on(consume_future(move_block_a));
    let _ = block_on(consume_future(move_block_b));
}

/// Drive async functions and async blocks via `block_on` and via a direct generic Future consumer.
pub fn drive_async_items() {
    // Via direct block_on.
    let sum = block_on(async_add(2, 3));
    assert_eq!(sum, 5);

    let greeting = block_on(async_greeting("fixture".to_string()));
    assert_eq!(greeting, "hello fixture");

    // Via generic Future bound.
    let sum2 = block_on(consume_future(async_add(10, 20)));
    assert_eq!(sum2, 30);

    // Locals crossing suspension.
    let crossed = block_on(local_crossing_suspension(4));
    assert_eq!(crossed, 13);

    async_blocks_demo();
    distinct_future_types_demo();
}
