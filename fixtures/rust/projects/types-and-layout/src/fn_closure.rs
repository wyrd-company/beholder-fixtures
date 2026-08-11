//! RS-CAN-TYPE-007 — function items, function pointers, and closures.

fn named_add(x: i32) -> i32 {
    x + 1
}

fn named_clone(x: i32) -> i32 {
    x + 1
}

fn generic_id<T>(value: T) -> T {
    value
}

unsafe fn unsafe_add(x: i32) -> i32 {
    x + 1
}

extern "C" fn extern_add(x: i32) -> i32 {
    x + 1
}

pub fn function_items_and_pointers() {
    // Each function has a unique zero-sized function-item type.
    let item_a = named_add;
    let item_b = named_clone;

    // Coercion to function pointer.
    let ptr_a: fn(i32) -> i32 = named_add;
    let ptr_b: fn(i32) -> i32 = item_a;

    // Two same-signature items coerce to the same pointer type.
    let _ = (ptr_a, ptr_b);

    // Items remain distinct at type level; pointers unify.
    assert_eq!(ptr_a(3), ptr_b(3));
    let _ = item_b;

    // Generic instantiations have distinct item types.
    let generic_i32: fn(i32) -> i32 = generic_id::<i32>;
    let generic_string: fn(String) -> String = generic_id::<String>;
    assert_eq!(generic_i32(5), 5);
    assert_eq!(generic_string("plot".to_string()), "plot");

    // Explicit pointer coercion from item.
    let explicit: fn(i32) -> i32 = named_add as fn(i32) -> i32;
    assert_eq!(explicit(9), 10);

    // Higher-ranked pointer (function pointer that accepts any lifetime).
    #[allow(clippy::needless_lifetimes)]
    fn hrtb_id<'a>(value: &'a i32) -> &'a i32 {
        value
    }
    let higher: for<'a> fn(&'a i32) -> &'a i32 = hrtb_id;
    let val = 11;
    assert_eq!(*higher(&val), 11);
}

pub fn closures_and_coercions() {
    // Noncapturing closure coerces to function pointer.
    let noncapturing = || 42_i32;
    let as_fn: fn() -> i32 = noncapturing;
    assert_eq!(as_fn(), 42);

    // Noncapturing closure with argument coerces similarly.
    let add_one = |x: i32| x + 1;
    let add_fn: fn(i32) -> i32 = add_one;
    assert_eq!(add_fn(5), 6);

    // Capturing closure retains its own anonymous type and cannot coerce.
    let base = 100_i32;
    let capturing = move |x: i32| x + base;
    assert_eq!(capturing(5), 105);
    // let bad: fn(i32) -> i32 = capturing; // would fail: capturing closure
    // does not coerce to a function pointer.

    // Move closure that happens to be Fn still distinct from FnOnce.
    let label = "field".to_string();
    let reader = move || label.clone();
    assert_eq!(reader(), "field");

    // Indirect calls through pointer.
    let target: fn(i32) -> i32 = named_add;
    assert_eq!(indirect_call(target, 7), 8);
}

fn indirect_call(f: fn(i32) -> i32, value: i32) -> i32 {
    f(value)
}

pub fn unsafe_and_extern_pointers() {
    let unsafe_ptr: unsafe fn(i32) -> i32 = unsafe_add;
    let extern_ptr: extern "C" fn(i32) -> i32 = extern_add;

    // Coercions remain ABI-aware; unsafe and extern are part of pointer identity.
    let _ = unsafe { unsafe_ptr(10) };
    assert_eq!(extern_ptr(10), 11);
}

pub fn join_point_coercion(valid: bool) -> fn(i32) -> i32 {
    // Coercion occurring at a `if` join point.
    if valid { named_add } else { named_clone }
}
