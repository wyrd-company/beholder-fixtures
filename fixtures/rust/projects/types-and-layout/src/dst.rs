//! RS-CAN-TYPE-008 — dynamically sized types, `?Sized`, trailing-slice struct, and metadata.

use std::fmt::Debug;

// Custom DST with trailing slice as the final field.
pub struct Trailer {
    pub header: u32,
    pub data: [u8],
}

// Helper that allocates a `Trailer` with the given payload length.
// Uses a stable transmute-based fat-pointer construction.
pub fn trailer_with_payload(header: u32, payload: &[u8]) -> Box<Trailer> {
    let len = payload.len();
    let bytes_needed = std::mem::size_of::<u32>() + len;
    let layout =
        std::alloc::Layout::from_size_align(bytes_needed, std::mem::align_of::<u32>()).unwrap();
    #[allow(clippy::unnecessary_cast)]
    let ptr = unsafe { std::alloc::alloc(layout) as *mut u8 };
    if ptr.is_null() {
        std::alloc::handle_alloc_error(layout);
    }
    unsafe {
        std::ptr::write(ptr as *mut u32, header);
        std::ptr::copy_nonoverlapping(payload.as_ptr(), ptr.add(std::mem::size_of::<u32>()), len);
        // Construct fat pointer via transmute of (data_ptr, len).
        let fat: *mut Trailer = std::mem::transmute::<(*mut u8, usize), *mut Trailer>((ptr, len));
        Box::from_raw(fat)
    }
}

// Another trailing-slice struct for local demonstrations.
pub struct SimpleTail {
    pub count: usize,
    pub items: [i32],
}

pub fn simple_tail_count(tail: &SimpleTail) -> usize {
    tail.count + tail.items.len()
}

pub fn accept_sized_and_unsized<T: ?Sized + Debug>(value: &T) {
    let _ = format!("{value:?}");
}

// Generic holder demonstrating `T: ?Sized` relaxation.
pub struct Holder<T: ?Sized> {
    pub boxed: Box<T>,
}

impl<T: ?Sized> Holder<T> {
    pub fn new(value: Box<T>) -> Self {
        Self { boxed: value }
    }
}

pub fn unsizing_examples() {
    let arr = [1_i32, 2, 3];
    let slice: &[i32] = &arr;
    assert_eq!(slice.len(), 3);

    let owned: String = "harvest".to_string();
    let as_str: &str = &owned;
    assert_eq!(as_str.len(), 7);

    let holder = SimpleHolder { value: 9_i32 };
    let as_dyn: &dyn Debug = &holder;
    let _ = format!("{as_dyn:?}");
    let _holder_small = Holder::new(Box::new(5_i32));
    let _holder_unsized: Holder<str> = Holder::new("meadow".to_string().into_boxed_str());
}

struct SimpleHolder {
    value: i32,
}

impl Debug for SimpleHolder {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "holder {}", self.value)
    }
}

pub fn pointer_metadata_examples() {
    let arr = [10_u8, 20, 30];
    let slice: &[u8] = &arr;
    assert_eq!(slice.len(), 3);
    // Slice DST metadata is its length, observable via `len()` / `size_of_val`.
    assert_eq!(std::mem::size_of_val(slice), 3);

    let owned: String = "plot".to_string();
    let as_str: &str = &owned;
    assert_eq!(as_str.len(), 4);
    assert_eq!(std::mem::size_of_val(as_str), 4);

    let value = SimpleHolder { value: 3 };
    let as_dyn: &dyn Debug = &value;
    // Trait-object metadata is a vtable pointer; size_of_val shows object size.
    let _ = std::mem::size_of_val(as_dyn);
    let _ = format!("{as_dyn:?}");
}

pub fn trailing_slice_access() {
    let boxed = trailer_with_payload(12, &[1, 2, 3, 4]);
    assert_eq!(boxed.header, 12);
    assert_eq!(boxed.data.len(), 4);
    assert_eq!(boxed.data[0], 1);
}
