//! RS-CAN-UNSAFE-003 — documented strict-provenance and address APIs.

use core::ptr;

/// Demonstrates the documented strict-provenance and address APIs:
/// `addr`, `expose_provenance`, `with_addr`, `map_addr`, and the free
/// functions `without_provenance` / `with_exposed_provenance`.
pub fn provenance_demo() {
    let value: u32 = 0xAABBCCDD;
    let ptr: *const u32 = &value as *const u32;

    // Documented address APIs (stable in 1.97): `addr` and `expose_provenance`
    // expose the address without stripping provenance semantics.
    let addr: usize = ptr.addr();
    let _exposed: usize = ptr.expose_provenance();

    // Re-derive a pointer with the same address and original provenance.
    let _with_addr: *const u32 = ptr.with_addr(addr);

    // Free function reconstituting provenance from an exposed address.
    let _from_exposed: *const u32 = ptr::with_exposed_provenance::<u32>(addr);

    // Pointer without provenance (address-only, must not be dereferenced
    // unless it happens to be valid without provenance).
    let _without: *const u32 = ptr::without_provenance::<u32>(addr);
    let _ = (_with_addr, _from_exposed, _without);
}

/// In-allocation arithmetic: `add`/`offset` stay within allocation bounds,
/// `wrapping_add` is distinct and documented as wrapping rather than
/// in-bounds. The valid fixture path uses strictly in-bounds arithmetic.
pub fn in_allocation_demo() {
    let buffer = [1u32, 2, 3, 4];
    let base: *const u32 = buffer.as_ptr();

    // SAFETY: `base.add(2)` stays in-bounds of `buffer` (len 4).
    let mid: *const u32 = unsafe { base.add(2) };
    assert_eq!(unsafe { *mid }, 3);

    // Pointer offset variants: `add` vs `wrapping_add` distinction.
    let _wrapping: *const u32 = base.wrapping_add(1);

    // `byte_add` style arithmetic via `add` on `*const u8` equivalent.
    let byte_base = base.cast::<u8>();
    // SAFETY: offset of 4 bytes stays within the 16-byte allocation.
    let _byte_mid = unsafe { byte_base.add(4) };
}

/// One-past-the-allocation pointers may be formed and compared but not
/// dereferenced. Valid in-allocation and one-past arithmetic and comparison.
pub fn one_past_demo() {
    let buffer = [10u32, 20, 30];
    let base: *const u32 = buffer.as_ptr();
    let end: *const u32 = unsafe { base.add(buffer.len()) };

    // Comparison of one-past with in-allocation base is validPointer comparison.
    assert!(base < end);
    assert_eq!(unsafe { base.add(buffer.len()) }, end);

    // `addr_eq` style comparison via `addr` is the documented strict-provenance
    // way to compare addresses without conflating provenance.
    let addr_base = base.addr();
    let addr_end = end.addr();
    assert!(addr_base < addr_end);
}

/// Pointer mapping that preserves provenance while transforming the address.
/// `map_addr` is the documented API for address tagging/masking without
/// fabricating provenance.
pub fn pointer_mapping_demo() {
    let value: u64 = 0x1234_5678;
    let ptr: *const u64 = &value as *const u64;

    // Tag low bits then mask, preserving original provenance.
    let tagged = ptr.map_addr(|addr| addr | 0b11);
    let masked = tagged.map_addr(|addr| addr & !0b11);

    // Round-trip preserves original address and provenance.
    assert_eq!(masked.addr(), ptr.addr());
    // Provenance-preserving mapping never leaves the original allocation.
    assert_eq!(masked, ptr.with_addr(ptr.addr()));
}
