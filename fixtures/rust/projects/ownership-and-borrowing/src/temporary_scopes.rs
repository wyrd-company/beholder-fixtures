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

/// `if let` temporary scope: a temporary created in the `if let` scrutinee is
/// dropped at a different point across editions. The scrutinee builds a
/// Drop-observable `Guard` temporary but yields `None`, so the `else` branch
/// runs. In edition 2024 the scrutinee temporary is dropped *before* the `else`
/// branch, so the `flag.get()` predicate reads `true`; in edition 2021 the same
/// temporary stays alive through the `else` branch, so the identical predicate
/// reads `false`. The paired 2021 crate runs the exact same predicate.
pub fn if_let_temporary() -> bool {
    let flag = Rc::new(Cell::new(false));
    struct Guard(Rc<Cell<bool>>);
    impl Drop for Guard {
        fn drop(&mut self) {
            self.0.set(true);
        }
    }
    impl Guard {
        fn as_none(&self) -> Option<&()> {
            None
        }
    }
    if let Some(_) = Guard(Rc::clone(&flag)).as_none() {
        false
    } else {
        // Edition 2024 drops the scrutinee `Guard` before this branch, so the
        // predicate is `true`; edition 2021 keeps it alive, so it is `false`.
        flag.get()
    }
}

/// Block tail temporary: the temporary produced by a block's tail expression is
/// dropped relative to the block's own locals differently across editions. The
/// tail expression builds a `Guard` temporary; an `Observer` local records
/// whether that temporary has already dropped when the local itself drops. In
/// edition 2024 the tail temporary drops *before* the block's locals, so the
/// observation is `true`; in edition 2021 it drops *after* the locals, so the
/// identical observation is `false`.
pub fn block_tail_temporary() -> bool {
    let flag = Rc::new(Cell::new(false));
    let observed = Rc::new(Cell::new(false));
    struct Guard(Rc<Cell<bool>>);
    impl Drop for Guard {
        fn drop(&mut self) {
            self.0.set(true);
        }
    }
    impl Guard {
        fn read(&self) -> bool {
            self.0.get()
        }
    }
    struct Observer(Rc<Cell<bool>>, Rc<Cell<bool>>);
    impl Drop for Observer {
        fn drop(&mut self) {
            // Record the tail temporary's drop state at local-drop time.
            self.1.set(self.0.get());
        }
    }
    let _tail_value = {
        let _observer = Observer(Rc::clone(&flag), Rc::clone(&observed));
        Guard(Rc::clone(&flag)).read()
    };
    observed.get()
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
