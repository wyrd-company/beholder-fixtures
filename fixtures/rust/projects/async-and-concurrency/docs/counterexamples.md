# Counterexamples (documentation only — never compiled)

Invalid Rust programs are not part of the corpus. Each item below is the
counterexample preserved beside the valid demonstration referenced.

## RS-CAN-ASYNC-001 — recursive async without indirection

```rust,ignore
// Recursive async without indirection is rejected: the future would need
// to contain itself, yielding infinite size. Use `Box` indirection instead.
// async fn recurse(n: u32) -> u32 { if n == 0 { 0 } else { recurse(n-1).await + 1 } }
```

## RS-CAN-ASYNC-002 — await outside async

```rust,ignore
// `.await` outside an async context is rejected.
// let x = PendingToReady::new(1).await; // error: `await` is only allowed inside `async` blocks and functions
// Lock guards across await are flagged by Clippy (`await_holding_lock`) but not
// a language rejection; the fixture avoids holding a lock guard across suspension.
```

## RS-CAN-ASYNC-003 — pointer escape undermining pin

```rust,ignore
// Escaping a raw pointer to pinned data and later moving through it violates
// the pin contract and is never executed.
// let mut not_unpinned = NotUnpinned::new(1);
// let pinned = Box::pin(not_unpinned);
// let raw: *mut NotUnpinned = unsafe { Pin::into_inner_unchecked(pinned) as *mut _ };
// unsafe { std::ptr::write(raw, NotUnpinned::new(2)); } // UB: moves pinned value
```

## RS-CAN-ASYNC-004 — lending future escape, move capture

```rust,ignore
// Lending future escaping the closure's borrow is rejected.
// let lending = async |x: &i32| x + 1;
// let fut = lending(&42).await; // borrow escapes if stored beyond call
// `async move` captures by value; subsequent use after move is rejected.
// let s = String::from("moved");
// let consuming = async move || s;
// consuming().await;
// let _ = s; // error: use after move
```

## RS-CAN-ASYNC-005 — body-only change breaking downstream Send

```rust,ignore
// Near-identical futures where one holds a non-Send value across await
// becomes `!Send` and would be rejected by a `Send` bound.
// let rc = Rc::new(1);
// async move { let _rc = rc; YieldOnce::new().await; } // !Send
// let rc2 = Rc::new(1);
// async move { let _v = *rc2; drop(rc2); YieldOnce::new().await; } // Send
// require_send(non_send_future); // error: future cannot be sent between threads safely
```

## RS-CAN-CONCUR-001 — borrowed non-scoped thread capture, non-Send spawn

```rust,ignore
// Borrowing into a non-scoped thread requires `'static` and is rejected.
// let data = vec![1,2,3];
// std::thread::spawn(|| data.len()); // error: closure may outlive current function
// Non-Send values cannot be sent to another thread.
// let rc = std::rc::Rc::new(1);
// std::thread::spawn(move || *rc); // error: `Rc` cannot be sent between threads safely
// Dropped join handle detaches — valid but nevers joins; see `threads::panic_and_join_demo`.
```

## RS-CAN-CONCUR-002 — invalid ordering, unsupported width, data race

```rust,ignore
// Invalid ordering: `Release` is not valid for `load`; `AcqRel` not valid for `load`.
// let x = AtomicU32::new(0);
// x.load(Ordering::Release); // error: invalid ordering for load
// x.store(1, Ordering::Acquire); // error: invalid ordering for store
// x.compare_exchange(0, 1, Ordering::Relaxed, Ordering::Release); // error: failure ordering invalid
// Unsupported width on targets without it — gated by `target_has_atomic`.
// Data races on non-atomic memory are undefined behavior and never executed:
// static mut UNSAFE_SHARED: i32 = 0;
// // concurrent unsynchronized read/write to `UNSAFE_SHARED` is UB
```

## Additional — data-race undefined behavior

Data-race undefined behavior is documented rather than executed. The fixture
never performs concurrent unsynchronized non-atomic access. All shared
mutation uses `Arc<Mutex<_>>` or atomics with defined orderings.

## Additional — temporary not crossing later await

Non-crossing temporaries and postfix/autoderef behavior around `.await` are
documented as semantic observations; they are valid edge cases that do not
require separate source beyond the suspension-borrow examples in
`src/await_polling.rs`.
