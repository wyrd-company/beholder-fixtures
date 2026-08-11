//! Edition 2021 member: disjoint closure capture, temporary scope (2021), and match ergonomics (2021).
#![allow(dead_code)]

use std::cell::Cell;
use std::rc::Rc;

pub struct Pair {
    pub first: String,
    pub second: String,
}

pub struct Container {
    pub value: String,
    pub count: u32,
}

// RS-CAN-OWN-006: disjoint field capture accepted in edition 2021.
pub fn capture_2021_disjoint() -> String {
    let mut pair = Pair {
        first: String::from("hello"),
        second: String::from("world"),
    };
    let closure = || pair.first.len();
    // Disjoint: `pair.second` not captured, so mutation while closure is live is allowed in 2021.
    pair.second.push_str("!");
    let _ = closure();
    pair.second
}

pub fn move_closure_2021() -> usize {
    let data = String::from("edition-2021");
    let closure = move || data.len();
    closure() + closure()
}

// RS-CAN-OWN-004: temporary scopes in edition 2021.
// In 2021, `if let` and block tail temporaries live longer than in 2024.
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

pub fn extending_borrow_2021() -> usize {
    let extended = &String::from("extended-2021");
    extended.len()
}

pub fn nonextending_borrow_2021() {
    let _ = &String::from("nonextending-2021");
}

pub fn match_scrutinee_temporary_2021() -> bool {
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

pub fn if_let_temporary_2021() -> bool {
    let flag = Rc::new(Cell::new(false));
    struct Guard(Rc<Cell<bool>>);
    impl Drop for Guard {
        fn drop(&mut self) {
            self.0.set(true);
        }
    }
    if let Some(_) = Some(&Guard(Rc::clone(&flag))) {
        // In edition 2021 the `&Guard` temporary from the condition lives into
        // the then block, so flag is still false here.
        !flag.get()
    } else {
        false
    }
}

pub fn block_tail_temporary_2021() -> bool {
    let flag = Rc::new(Cell::new(false));
    struct Guard(Rc<Cell<bool>>);
    impl Drop for Guard {
        fn drop(&mut self) {
            self.0.set(true);
        }
    }
    let after_block_still_alive = {
        let _ptr = { &Guard(Rc::clone(&flag)) as *const Guard };
        !flag.get()
    };
    after_block_still_alive && !flag.get()
}

pub fn destructor_order_2021() -> Vec<&'static str> {
    {
        let _a = Droppable("first-2021");
        let _b = Droppable("second-2021");
        let _c = Droppable("third-2021");
    }
    take_order()
}

// RS-CAN-OWN-008: match ergonomics in edition 2021 allows explicit `ref`/`ref mut` under inherited modes.
pub fn inferred_binding_modes_2021() -> (String, u32) {
    let owned = Container {
        value: String::from("owned-2021"),
        count: 1,
    };
    let (moved, copied) = match owned {
        Container { value, count } => (value, count),
    };
    (moved, copied)
}

pub fn explicit_binding_modes_2021() -> usize {
    let container = Container {
        value: String::from("explicit-2021"),
        count: 5,
    };
    match &container {
        Container {
            ref value,
            ref count,
        } => value.len() + *count as usize,
    }
}

pub fn ref_mut_binding_2021() -> String {
    let mut container = Container {
        value: String::from("mut-2021"),
        count: 0,
    };
    match &mut container {
        Container {
            ref mut value,
            ref mut count,
        } => {
            value.push_str("!");
            *count += 1;
        }
    }
    container.value
}

pub fn edition_id() -> &'static str {
    "2021"
}
