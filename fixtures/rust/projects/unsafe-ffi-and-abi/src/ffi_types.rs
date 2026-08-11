//! RS-CAN-FFI-003 — FFI-safe layouts, handles, callbacks, and ownership.

use core::ffi::c_void;
use core::ptr::NonNull;

/// `repr(C)` struct that can cross a C-ABI boundary.
#[repr(C)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FfiRecord {
    pub id: u32,
    pub flag: u8,
    pub pad: [u8; 3],
    pub value: i32,
}

/// `repr(C)` union with overlapping fields, passed by value across FFI.
#[repr(C)]
pub union FfiUnion {
    pub as_u32: u32,
    pub as_i32: i32,
    pub bytes: [u8; 4],
}

/// Integer-repr enum passed across FFI (fieldless, `repr(u32)`).
#[repr(u32)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FfiKind {
    Alpha = 1,
    Beta = 2,
    Gamma = 3,
}

/// Opaque handle: incomplete type behind a raw pointer.
/// The pointee `OpaqueInner` is never defined, so callers cannot construct
/// or inspect the object, only pass handles.
#[repr(C)]
pub struct OpaqueHandle {
    _private: [u8; 0],
    _marker: core::marker::PhantomData<(*mut u8, core::marker::PhantomPinned)>,
}

/// Owned allocation backing an opaque handle.
pub struct HandleOwner {
    data: u32,
}

impl HandleOwner {
    pub fn new(value: u32) -> Self {
        Self { data: value }
    }

    pub fn as_handle(&mut self) -> *mut OpaqueHandle {
        &mut self.data as *mut u32 as *mut OpaqueHandle
    }

    pub fn value(handle: *mut OpaqueHandle) -> u32 {
        // SAFETY: `handle` was produced by `as_handle` from a live `HandleOwner`.
        unsafe { *(handle as *mut u32) }
    }
}

/// Nullable pointer via `Option<NonNull<T>>` (niche-optimized, null = None).
pub fn nullable_pointer_demo() -> Option<NonNull<u32>> {
    let mut value: u32 = 99;
    // SAFETY: `value` lives for the duration of this demo; the returned
    // `NonNull` is produced from a live reference. The None case is also shown.
    let some = NonNull::new(&mut value as *mut u32);
    let none: Option<NonNull<u32>> = None;
    // Use both to keep the nullable-pointer identity observable.
    if none.is_none() { some } else { none }
}

/// Nullable function pointer (`Option<extern "C" fn>`) where None is null.
pub type NullableCallback = Option<extern "C" fn(i32) -> i32>;

extern "C" fn sample_callback(x: i32) -> i32 {
    x.wrapping_add(1)
}

pub fn nullable_fn_demo() -> (NullableCallback, NullableCallback) {
    (Some(sample_callback), None)
}

/// Callback type for FFI. `extern "C" fn` with a context pointer.
pub type FfiCallback = extern "C" fn(i32, *mut c_void) -> i32;

extern "C" fn double_callback(value: i32, _ctx: *mut c_void) -> i32 {
    value.wrapping_mul(2)
}

/// Function that takes a C-ABI callback and invokes it.
pub fn invoke_callback(cb: FfiCallback, value: i32, ctx: *mut c_void) -> i32 {
    cb(value, ctx)
}

/// Demonstrate passing `repr(C)` struct, union, and integer enum across a
/// logical FFI boundary expressed as `extern "C"` functions in this crate.
#[unsafe(no_mangle)]
pub extern "C" fn ffi_record_roundtrip(rec: FfiRecord) -> FfiRecord {
    rec
}

#[unsafe(no_mangle)]
pub extern "C" fn ffi_union_as_u32(u: FfiUnion) -> u32 {
    // SAFETY: caller guarantees the union was written as `as_u32`.
    unsafe { u.as_u32 }
}

#[unsafe(no_mangle)]
pub extern "C" fn ffi_kind_label(kind: FfiKind) -> u32 {
    kind as u32
}

/// Aggregate entry covering all FFI-003 identities so that `fixture_overview`
/// observes them.
pub fn ffi_types_demo() -> u32 {
    let rec = FfiRecord {
        id: 1,
        flag: 1,
        pad: [0; 3],
        value: -7,
    };
    let back = ffi_record_roundtrip(rec);
    assert_eq!(back.id, 1);

    let u = FfiUnion { as_u32: 0x01020304 };
    assert_eq!(ffi_union_as_u32(u), 0x01020304);

    assert_eq!(ffi_kind_label(FfiKind::Beta), 2);

    // Opaque handle round trip.
    let mut owner = HandleOwner::new(123);
    let handle = owner.as_handle();
    assert_eq!(HandleOwner::value(handle), 123);

    // Nullable pointer and fn pointer identities.
    let _ = nullable_pointer_demo();
    let _ = nullable_fn_demo();

    back.value as u32
}

/// Callback demo: pass a C callback and invoke it.
pub fn callback_demo() -> i32 {
    invoke_callback(double_callback, 21, core::ptr::null_mut())
}
