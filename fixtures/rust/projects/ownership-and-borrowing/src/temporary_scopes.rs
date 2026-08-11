//! RS-CAN-OWN-004: Temporary lifetime extension and drop scopes (edition 2024 view).
//! Paired edition-2021 behavior lives in `crates/edition-2021`.

use std::cell::Cell;
use std::rc::Rc;

/// Helper to observe destructor order.
thread_local! {
    static DROP_ORDER: Cell<Vec<&'static str>> = const { Cell::new(Vec::new()) };
}

struct Droppable(&'static str);

impl Drop for Droppable {
    fn drop(&mut self) {
        DROP_ORDER.with(|c| {
            let mut v = c.take();
            v.push(self.0);
            c.set(v);
        });
    }
}

fn take_order() -> Vec<&'static str> {
    DROP_ORDER.with(|c| c.take())
}

/// Extending borrow: `let x = &String::from(...)` extends temporary to scope end.
pub fn extending_borrow() -> usize {
    let extended = &String::from("extended");
    extended.len()
}

/// Non-extending borrow: `let _ = &String::from(...)` does not extend; temporary drops immediately.
pub fn nonextending_borrow() {
    let _ = &String::from("nonextending");
}

/// Match scrutinee temporary: Drop-observable temporary in `match` scrutinee.
/// The temporary `&Guard` created in the scrutinee lives for the whole `match`.
pub fn match_scrutinee_temporary() -> bool {
    let flag = Rc::new(Cell::new(false));
    struct Guard(Rc<Cell<bool>>);
    impl Drop for Guard {
        fn drop(&mut self) {
            self.0.set(true);
        }
    }
    let inside_alive = match &Guard(Rc::clone(&flag)) {
        _ => !flag.get(),
    };
    inside_alive && flag.get()
}

/// `if let` temporary scope: edition 2024 narrows the temporaries created in the
/// condition so they are dropped before the `then` block. The paired 2021 crate
/// keeps the same syntax but the temporary lives into the block.
pub fn if_let_temporary() -> bool {
    let flag = Rc::new(Cell::new(false));
    struct Guard(Rc<Cell<bool>>);
    impl Drop for Guard {
        fn drop(&mut self) {
            self.0.set(true);
        }
    }
    if let Some(_) = Some(&Guard(Rc::clone(&flag))) {
        // In edition 2024 the `&Guard` temporary from the condition is dropped
        // before entering this block, so flag is true.
        flag.get()
    } else {
        false
    }
}

/// Block tail temporary: a reference to a temporary produced as the tail
/// expression of a block. In edition 2024 the tail temporary's scope ends at the
/// block boundary, while in edition 2021 it was extended.
pub fn block_tail_temporary() -> bool {
    let flag = Rc::new(Cell::new(false));
    struct Guard(Rc<Cell<bool>>);
    impl Drop for Guard {
        fn drop(&mut self) {
            self.0.set(true);
        }
    }
    let after_block_dropped = {
        let _ptr = { &Guard(Rc::clone(&flag)) as *const Guard };
        flag.get()
    };
    after_block_dropped && flag.get()
}

/// Function return temporary: temporary in return expression lives until end of function.
pub fn function_return_temporary() -> String {
    String::from("return-temp")
}

/// Destructor order: drops happen in reverse declaration order at scope end.
pub fn destructor_order() -> Vec<&'static str> {
    let _a = Droppable("a");
    let _b = Droppable("b");
    let _c = Droppable("c");
    Vec::new()
}

/// Inner version that captures drop order.
pub fn destructor_order_inner() -> Vec<&'static str> {
    {
        let _a = Droppable("first");
        let _b = Droppable("second");
        let _c = Droppable("third");
    }
    take_order()
}

pub fn temporary_scopes_summary() -> (usize, bool, bool, bool, String, Vec<&'static str>) {
    let a = extending_borrow();
    nonextending_borrow();
    let b = match_scrutinee_temporary();
    let c = if_let_temporary();
    let d = block_tail_temporary();
    let e = function_return_temporary();
    let f = destructor_order_inner();
    let _ = destructor_order();
    (a, b, c, d, e, f)
}
