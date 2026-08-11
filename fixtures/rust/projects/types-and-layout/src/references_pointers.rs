//! RS-CAN-TYPE-006 — references, raw pointers, and mutability.

use std::ptr::{self, NonNull};

#[allow(clippy::borrow_deref_ref)]
pub fn shared_and_mutable_refs() {
    let mut value = 10_i32;
    let shared: &i32 = &value;
    let reborrow: &i32 = &*shared;
    assert_eq!(*reborrow, 10);

    {
        let mutable: &mut i32 = &mut value;
        *mutable = 20;
        // Mutable-to-shared reborrow within the same exclusive region.
        let second: &i32 = &*mutable;
        assert_eq!(*second, 20);
    }
    assert_eq!(value, 20);

    // Overlapping borrows via scoped region.
    let mut data = [1, 2, 3];
    let first = &data[0];
    assert_eq!(*first, 1);
    // Shared use ends; mutable use resumes.
    data[0] = 42;
    assert_eq!(data[0], 42);
}

pub fn raw_formation_and_deref() {
    let mut value = 100_i32;

    // Raw formation from references (documented APIs only).
    let const_ptr: *const i32 = ptr::addr_of!(value);
    let mut_ptr: *mut i32 = ptr::addr_of_mut!(value);

    // `&raw` formation avoids intermediate reference.
    let raw_const = &raw const value;
    let raw_mut = &raw mut value;
    assert_eq!(unsafe { *raw_const }, 100);
    let _ = raw_mut;

    // Explicit null pointer APIs.
    let null: *const i32 = ptr::null();
    assert!(null.is_null());
    let null_mut: *mut i32 = ptr::null_mut();
    assert!(null_mut.is_null());

    // NonNull wrappers.
    let non_null = NonNull::from(&value);
    assert_eq!(unsafe { *non_null.as_ptr() }, 100);

    // Unsafe dereference of raw pointers.
    unsafe {
        assert_eq!(*const_ptr, 100);
        *mut_ptr = 200;
        assert_eq!(*const_ptr, 200);
    }

    // Restore.
    value = 100;
    let _ = value;
}

pub fn raw_pointer_api_variants() {
    let stack = 5_i32;
    // addr_of with field projection.
    let holder = (stack, "field".to_string());
    let field_ptr: *const i32 = ptr::addr_of!(holder.0);
    assert_eq!(unsafe { *field_ptr }, 5);

    // From ref raw formation preserves provenance-free address for demo.
    let r: &i32 = &stack;
    let through_raw: *const i32 = r as *const i32;
    assert_eq!(unsafe { *through_raw }, 5);
}

pub fn misaligned_and_packaged_doc() {
    // Unaligned packed-field, dangling, null-reborrow, and aliasing
    // counterexamples are documented in `docs/counterexamples.md`; no invalid
    // reference is executed here.
}
