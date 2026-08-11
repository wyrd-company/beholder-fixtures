//! RS-CAN-OWN-001: Moves, move paths, and partial moves.

/// Inventory with mixed ownership properties.
pub struct Inventory {
    pub name: String,
    pub quantity: u32,
    pub label: String,
}

/// Drop type to illustrate field-move restriction (moving a field out of a
/// type that implements `Drop` requires careful handling; partial moves
/// are still possible via destructuring when the type is not dropped afterward).
pub struct WithDrop {
    pub owned: String,
    pub count: u32,
}

impl Drop for WithDrop {
    fn drop(&mut self) {}
}

/// Destructure moving one field while borrowing or copying another.
/// `quantity` is `Copy`, so it copies rather than moves. `label` is borrowed.
pub fn destructure_move_and_borrow() -> (String, u32) {
    let inv = Inventory {
        name: String::from("widget"),
        quantity: 42,
        label: String::from("blue"),
    };
    // Move `name`, copy `quantity`, borrow `label`.
    let Inventory {
        name: moved_name,
        quantity,
        ref label,
    } = inv;
    let borrowed_len = label.len();
    let _ = borrowed_len;
    // `quantity` was copied, `moved_name` was moved. Remaining borrow ends before return.
    (moved_name, quantity)
}

/// Demonstrate that after a partial move, unaffected paths remain usable,
/// while the moved path is consumed.
pub fn partial_move_remaining_usable() -> String {
    let inv = Inventory {
        name: String::from("gadget"),
        quantity: 7,
        label: String::from("red"),
    };
    let Inventory {
        name,
        quantity,
        label,
    } = inv;
    // `name` moved, others remain.
    let _ = quantity;
    let _ = label.len();
    name
}

/// Moves through dereference.
pub fn move_through_deref() -> String {
    let boxed = Box::new(Inventory {
        name: String::from("boxed"),
        quantity: 1,
        label: String::from("tag"),
    });
    // Move field through dereference of Box.
    let name = (*boxed).name;
    name
}

/// Explicit copies: `Copy` fields are copied, non-`Copy` fields move.
pub fn explicit_copy_demo() -> (u32, u32) {
    let a: u32 = 10;
    let b = a; // copy
    let c = a; // `a` still usable because `u32: Copy`
    (b, c)
}

/// Branch-dependent initialization: each branch initializes the same binding.
pub fn branch_init_demo(cond: bool) -> String {
    let value;
    if cond {
        value = String::from("alpha");
    } else {
        value = String::from("beta");
    }
    value
}

/// Closure capture moving a value.
pub fn closure_move_capture() -> usize {
    let s = String::from("capture");
    let consume = move || s.len();
    // `s` moved into closure; closure itself owns it.
    consume()
}

/// Whole-value use after move is documented as a counterexample, not compiled.
/// See `docs/counterexamples.md` for the invalid `let x = inv; let y = inv;` pattern.

pub fn moves_summary() -> (&'static str, String, u32) {
    let (moved, copied) = destructure_move_and_borrow();
    let via_box = move_through_deref();
    let _ = partial_move_remaining_usable();
    let _ = explicit_copy_demo();
    let _ = branch_init_demo(true);
    let _ = closure_move_capture();
    let _ = via_box.len();
    ("moves_partial_moves", moved, copied)
}
