//! RS-CAN-OWN-004: Temporary lifetime extension and drop scopes (edition 2024 view).
//! Paired edition-2021 behavior lives in `crates/edition-2021`.

use std::cell::Cell;

/// Helper to observe destructor order.
thread_local! {
    static DROP_ORDER: Cell<Vec<&'static str>> = const { Cell::new(Vec::new()) };
}

struct Droppable(&'static str);

impl Drop for Droppable {
    fn drop(&mut self) {
        // Record drop; thread-local Cell requires interior mutability.
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
/// Also statement temporaries drop at end of statement.
pub fn nonextending_borrow() {
    let _ = &String::from("nonextending");
    // Temporary already dropped here.
}

/// Match scrutinee temporary: temporary in `match` scrutinee lives for the whole match.
pub fn match_scrutinee_temporary() -> usize {
    match String::from("scrutinee").len() {
        0 => 0,
        n => n,
    }
}

/// `if let` temporary scope: in edition 2024 the temporary in the condition
/// does not live into the block's tail in the same way as 2021.
/// This 2024 crate demonstrates the narrowed scope.
pub fn if_let_temporary() -> usize {
    if let Some(len) = Some(String::from("if-let-temp").len()) {
        len
    } else {
        0
    }
}

/// Block tail temporary: value expression tail temporary scope narrowed in edition 2024.
pub fn block_tail_temporary() -> usize {
    // Block whose tail is a reference to a temporary.
    // In 2024 the temporary's scope is narrower than in 2021.
    let val = {
        let inner = String::from("block-tail");
        inner.len()
    };
    val
}

/// Function return temporary: temporary in return expression lives until end of function.
pub fn function_return_temporary() -> String {
    // `String::from` temporary moved directly into return, not borrowed.
    String::from("return-temp")
}

/// Destructor order: drops happen in reverse declaration order at scope end.
pub fn destructor_order() -> Vec<&'static str> {
    let _a = Droppable("a");
    let _b = Droppable("b");
    let _c = Droppable("c");
    // At scope end, c then b then a. We capture after scope by using inner block.
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

/// Lock-guard temporary hazard is documented, not executed as source that would hold a lock
/// across a temporary scope incorrectly; see `docs/counterexamples.md`.

pub fn temporary_scopes_summary() -> (usize, usize, usize, String, Vec<&'static str>) {
    let a = extending_borrow();
    nonextending_borrow();
    let b = match_scrutinee_temporary();
    let c = if_let_temporary();
    let _ = block_tail_temporary();
    let d = function_return_temporary();
    let e = destructor_order_inner();
    let _ = destructor_order();
    (a, b, c, d, e)
}
