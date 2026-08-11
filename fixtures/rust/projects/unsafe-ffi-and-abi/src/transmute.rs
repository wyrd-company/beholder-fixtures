//! RS-CAN-UNSAFE-004 — justified transparent-wrapper transmute.

use core::mem::transmute;

/// Transparent wrapper with guaranteed identical layout to its single field.
#[repr(transparent)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Wrapper(pub u32);

/// Second transparent wrapper over the same inner type, layout-compatible.
#[repr(transparent)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct OtherWrapper(pub u32);

/// Inner payload for niche-aware transparent wrapper demo.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Inner(pub core::num::NonZeroU32);

#[repr(transparent)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TransparentInner(pub Inner);

/// Justified transmute: transparent wrapper to inner and between wrappers.
/// Each direction is valid because the types have identical size, alignment,
/// and validity (both wrap a `u32`/`NonZeroU32`-compatible payload).
pub fn transparent_transmute_demo() -> (u32, u32, u32) {
    let wrapped = Wrapper(0x0A0B0C0D);
    // SAFETY: `Wrapper` is `repr(transparent)` over `u32`, so bit-identical.
    let inner: u32 = unsafe { transmute::<Wrapper, u32>(wrapped) };
    // SAFETY: `OtherWrapper` is also transparent over `u32` with same layout.
    let other: OtherWrapper = unsafe { transmute::<Wrapper, OtherWrapper>(wrapped) };
    // SAFETY: round-trip through `Inner`/`TransparentInner` preserves niche.
    let niche = Inner(core::num::NonZeroU32::new(41).unwrap());
    let transparent = TransparentInner(niche);
    let back: Inner = unsafe { transmute::<TransparentInner, Inner>(transparent) };
    assert_eq!(niche, back);
    (inner, other.0, back.0.get())
}

/// Safer alternative to transmute for the same conversion, retained to
/// document that transmute is not the only path and that size/validity must
/// still hold for either technique.
pub fn safer_alternative(wrapped: Wrapper) -> u32 {
    // Deconstruct rather than transmute when the layout happens to be known.
    wrapped.0
}
