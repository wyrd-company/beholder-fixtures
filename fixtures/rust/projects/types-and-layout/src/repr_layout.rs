//! RS-CAN-TYPE-013 — representation and layout attributes.

// Explicit `repr(Rust)` leaves order and padding unspecified.
#[repr(Rust)]
#[derive(Debug, PartialEq)]
pub struct RustLayout {
    pub a: u8,
    pub b: u32,
    pub c: u16,
}

// Generic representation: layout guarantees carry through instantiations.
#[repr(C)]
#[derive(Debug, PartialEq)]
pub struct GenericC<T> {
    pub tag: u32,
    pub payload: T,
}

// C-compatible layout.
#[repr(C)]
#[derive(Debug, PartialEq)]
pub struct CLayout {
    pub a: u8,
    pub b: u32,
    pub c: u16,
}

// Integer repr for fieldless enum.
#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SmallRepr {
    Alpha = 1,
    Beta = 2,
    Gamma = 10,
}

// Larger integer repr.
#[repr(i16)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SignedRepr {
    Negative = -5,
    Zero = 0,
    Positive = 7,
}

// Transparent wrapper guarantees single-field layout identity.
#[repr(transparent)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Transparent(pub u32);

// Packed layout: no padding, unaligned fields require copy.
#[repr(C, packed)]
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Packed {
    pub tag: u8,
    pub value: u32,
}

// Aligned layout.
#[repr(C, align(8))]
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Aligned {
    pub first: u8,
    pub second: u16,
}

// C-compatible tagged struct passed across a logical FFI boundary.
#[repr(C)]
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Crossing {
    pub id: u32,
    pub kind: SmallRepr,
}

extern "C" fn accepts_crossing(payload: Crossing) -> u32 {
    payload.id + payload.kind as u32
}

pub fn layout_observations() {
    // Size/alignment/offset only asserted where layout is guaranteed.
    assert_eq!(
        std::mem::size_of::<Transparent>(),
        std::mem::size_of::<u32>()
    );
    assert_eq!(
        std::mem::align_of::<Transparent>(),
        std::mem::align_of::<u32>()
    );

    assert_eq!(std::mem::align_of::<Aligned>(), 8);

    // repr(C) field offsets are defined by target C ABI; stable offset check.
    assert_eq!(std::mem::offset_of!(CLayout, a), 0);

    // repr(u8) enum size is exactly 1 byte.
    assert_eq!(std::mem::size_of::<SmallRepr>(), 1);
    assert_eq!(std::mem::size_of::<SignedRepr>(), 2);

    // Niche-like transparent generic instance: transparent Option-like case is
    // valid but niche layout itself is not asserted here.
    let wrapped = Transparent(5);
    assert_eq!(wrapped.0, 5);
}

pub fn packed_access_examples() {
    let packed = Packed {
        tag: 1,
        value: 0x1234_5678,
    };
    // Copy the field instead of creating an unaligned reference.
    let copied = { packed.value };
    assert_eq!(copied, 0x1234_5678);

    // Explicit copy via raw pointer with unaligned read.
    let unaligned = unsafe { std::ptr::addr_of!(packed.value).read_unaligned() };
    assert_eq!(unaligned, 0x1234_5678);
}

pub fn ffi_crossing_example() {
    let payload = Crossing {
        id: 7,
        kind: SmallRepr::Beta,
    };
    assert_eq!(accepts_crossing(payload), 9);
}

pub fn generic_repr_instance() {
    // Generic instances retain repr guarantees.
    let c = CLayout { a: 1, b: 2, c: 3 };
    let generic_u32 = GenericC {
        tag: 1,
        payload: 7_u32,
    };
    let generic_u8 = GenericC {
        tag: 2,
        payload: 9_u8,
    };
    let ru = RustLayout { a: 1, b: 2, c: 3 };
    assert_eq!(
        std::mem::size_of_val(&generic_u32),
        std::mem::size_of::<u32>() * 2
    );
    let _ = (c, generic_u8, ru);
}
