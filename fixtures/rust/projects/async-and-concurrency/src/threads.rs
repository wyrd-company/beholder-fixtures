//! RS-CAN-CONCUR-001 — threads, scoped borrowing, and join behavior.
#![allow(clippy::useless_vec)]

use std::sync::{Arc, Mutex};
use std::thread;

/// Move owned data to a thread and return the joined result.
pub fn move_owned_to_thread() -> String {
    let owned = String::from("owned-payload");
    let handle = thread::spawn(move || {
        // `owned` is moved into the thread.
        format!("thread: {owned}")
    });
    handle.join().expect("thread panicked")
}

/// Borrow data for the duration of a scoped thread set without requiring `'static`.
pub fn scoped_borrow_demo() -> usize {
    let data = vec![1, 2, 3, 4, 5];
    let mut sum = 0;

    thread::scope(|scope| {
        // Scoped borrow: `&data` is borrowed across the scope and each thread
        // is guaranteed to join before the scope exits.
        let handle_a = scope.spawn(|| data.iter().sum::<i32>());
        let handle_b = scope.spawn(|| data.len() as i32);
        let a = handle_a.join().expect("thread a panicked");
        let b = handle_b.join().expect("thread b panicked");
        sum = (a + b) as usize;
    });

    // `data` is accessible again after the scope.
    assert_eq!(data.len(), 5);
    sum
}

/// Require `Sync` for shared access across threads.
pub fn sync_requirement_demo() -> i32 {
    let shared = Arc::new(Mutex::new(0_i32));
    let shared_clone = Arc::clone(&shared);

    let handle = thread::spawn(move || {
        // `Arc<Mutex<i32>>` is `Sync` + `Send`, allowing shared mutation.
        let mut guard = shared_clone.lock().expect("lock poisoned");
        *guard += 10;
        *guard
    });

    let _ = handle.join().expect("thread panicked");
    let guard = shared.lock().expect("lock poisoned");
    *guard
}

/// Inspect panic and join results from threads.
pub fn panic_and_join_demo() {
    // Successful join.
    let ok = thread::spawn(|| 42_i32).join();
    assert!(ok.is_ok());
    assert_eq!(ok.unwrap(), 42);

    // Panicking thread returns `Err` on join.
    let panicking = thread::spawn(|| panic!("intentional fixture panic"));
    let err = panicking.join();
    assert!(err.is_err());
    let payload = err.unwrap_err();
    // Panic payload is `Box<dyn Any + Send>`; downcast to string for inspection.
    let message = payload
        .downcast_ref::<&str>()
        .copied()
        .or_else(|| payload.downcast_ref::<String>().map(|s| s.as_str()))
        .unwrap_or("<non-string panic>");
    assert!(message.contains("intentional fixture panic"));

    // Dropped join handle detaches rather than joining — documented in
    // `docs/counterexamples.md`. The thread continues detached; the fixture
    // does not rely on its completion.
    let detached_value = Arc::new(Mutex::new(0));
    let detached_clone = Arc::clone(&detached_value);
    let detached_handle = thread::spawn(move || {
        let mut guard = detached_clone.lock().expect("lock poisoned");
        *guard = 7;
    });
    // Intentionally not joining; detaching by dropping the handle.
    drop(detached_handle);
    // Give the detached thread a moment to complete before checking.
    thread::sleep(std::time::Duration::from_millis(20));
    // The detached thread may or may not have updated the value before this read,
    // but the operation itself is valid and demonstrates detached semantics.
    let _ = *detached_value.lock().expect("lock poisoned");
}

pub fn threads_demo() {
    let moved = move_owned_to_thread();
    assert_eq!(moved, "thread: owned-payload");

    let scoped_sum = scoped_borrow_demo();
    assert_eq!(scoped_sum, 20);

    let synced = sync_requirement_demo();
    assert_eq!(synced, 10);

    panic_and_join_demo();
}
