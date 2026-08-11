//! RS-CAN-TYPE-015 — the fixed coercion set at designated coercion sites.

use std::ops::Deref;

struct Wrapper(String);

impl Deref for Wrapper {
    type Target = str;
    fn deref(&self) -> &str {
        &self.0
    }
}

fn takes_str(value: &str) -> usize {
    value.len()
}

fn takes_fn_ptr(f: fn(i32) -> i32) -> i32 {
    f(5)
}

fn named_target(x: i32) -> i32 {
    x + 1
}

pub fn function_and_closure_coercions() {
    // Function-item to function-pointer coercion at a coercion site.
    let as_ptr: fn(i32) -> i32 = named_target;
    assert_eq!(as_ptr(3), 4);

    // Noncapturing closure to function pointer.
    let closure = |x: i32| x + 2;
    let via_closure: fn(i32) -> i32 = closure;
    assert_eq!(via_closure(3), 5);

    // Same closure outside a coercion site remains its own type.
    let direct = named_target;
    let _ = direct;
}

pub fn reference_coercions() {
    let mut value = 9_i32;
    let mutable: &mut i32 = &mut value;
    // Mutable to shared coercion at function call site.
    let shared: &i32 = mutable;
    assert_eq!(*shared, 9);

    // Nested coercion site inside block and branch propagates.
    #[allow(clippy::if_same_then_else)]
    let result: &i32 = { if true { &value } else { &value } };
    assert_eq!(*result, 9);
}

pub fn deref_and_unsizing() {
    // &String -> &str via deref coercion.
    let owned = "meadow".to_string();
    let borrowed: &str = &owned;
    assert_eq!(borrowed.len(), 6);

    // Deref through custom type.
    let wrapped = Wrapper("field".to_string());
    let len = takes_str(&wrapped);
    assert_eq!(len, 5);

    // &Box<String> -> &str via deref chain + unsizing.
    let boxed = Box::new("harvest".to_string());
    let as_str: &str = &boxed;
    assert_eq!(as_str, "harvest");

    // Array to slice unsizing.
    let arr: [i32; 3] = [1, 2, 3];
    let slice: &[i32] = &arr;
    assert_eq!(slice.len(), 3);

    // Unsize smart pointers: Box<[T; N]> -> Box<[T]>.
    let boxed_array: Box<[i32; 3]> = Box::new([4, 5, 6]);
    let unsized_box: Box<[i32]> = boxed_array;
    assert_eq!(unsized_box.len(), 3);

    // Rc unsizing similarly valid via coercion.
    let rc_array: std::rc::Rc<[i32; 2]> = std::rc::Rc::new([7, 8]);
    let rc_slice: std::rc::Rc<[i32]> = rc_array;
    assert_eq!(rc_slice.len(), 2);
}

pub fn branch_and_block_coercions() {
    // Least-upper-bound branch coercion: both arms coerce to `&str`.
    let owned_a = "alpha".to_string();
    let owned_b = "beta".to_string();
    let chosen: &str = if true { &owned_a } else { &owned_b };
    assert!(chosen.len() >= 4);

    // Block tail coercion propagates through coercion site.
    let value: &str = {
        let temp = "plot".to_string();
        // Box dereferences to str via temporary.
        Box::leak(Box::new(temp)).as_str()
    };
    assert_eq!(value, "plot");
    // Leak is intentional for coercion illustration; reclaim not needed in fixture.
}

pub fn method_receiver_adjustments() {
    // Method receiver adjustment is distinct from ordinary function argument coercion.
    let owned = "field".to_string();
    assert_eq!(owned.len(), 5); // method autoderef + borrow
    // Equivalent function call requires explicit borrow coercion.
    assert_eq!(takes_str(&owned), 5);
    assert_eq!(takes_fn_ptr(named_target), 6);
}
