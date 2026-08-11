//! RS-CAN-TRAIT-013 — derive-generated standard impls and bounds.

#![allow(clippy::non_canonical_clone_impl, clippy::clone_on_copy)]

use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use std::marker::PhantomData;

/// Struct with derived standard traits where generic param is used directly.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Default)]
pub struct DerivedGeneric<T> {
    pub value: T,
}

/// Enum with derived traits across variants.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum DerivedEnum<T> {
    Unit,
    Single(T),
    Pair(T, T),
}

impl<T> Default for DerivedEnum<T>
where
    T: Default,
{
    fn default() -> Self {
        Self::Single(T::default())
    }
}

/// Another derived set for comparison.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Default)]
pub struct DerivedWithCustomDefault {
    pub a: i32,
    pub b: String,
}

impl PartialOrd for DerivedWithCustomDefault {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for DerivedWithCustomDefault {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.a.cmp(&other.a).then(self.b.cmp(&other.b))
    }
}

/// Derive adds an unnecessary bound when `T` is only phantom: `DerivedPhantom<T>`
/// derives `Clone` with `T: Clone` even though `T` is not stored.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Default)]
pub struct DerivedPhantom<T>(PhantomData<T>);

/// Manual implementation that avoids the unnecessary generic bound.
/// `ManualPhantom<T>` stores only a `u32` plus phantom, so its traits do not require `T`.
pub struct ManualPhantom<T> {
    pub value: u32,
    _marker: PhantomData<T>,
}

impl<T> ManualPhantom<T> {
    pub fn new(value: u32) -> Self {
        Self {
            value,
            _marker: PhantomData,
        }
    }
}

impl<T> Clone for ManualPhantom<T> {
    fn clone(&self) -> Self {
        Self::new(self.value)
    }
}

impl<T> Copy for ManualPhantom<T> {}

impl<T> std::fmt::Debug for ManualPhantom<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ManualPhantom")
            .field("value", &self.value)
            .finish()
    }
}

impl<T> PartialEq for ManualPhantom<T> {
    fn eq(&self, other: &Self) -> bool {
        self.value == other.value
    }
}

impl<T> Eq for ManualPhantom<T> {}

impl<T> PartialOrd for ManualPhantom<T> {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl<T> Ord for ManualPhantom<T> {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.value.cmp(&other.value)
    }
}

impl<T> Hash for ManualPhantom<T> {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.value.hash(state);
    }
}

impl<T> Default for ManualPhantom<T> {
    fn default() -> Self {
        Self::new(0)
    }
}

/// A type that intentionally avoids deriving Copy to show manual bound control:
/// `Copy` requires `T: Copy` but we provide manual `Copy` only when desired.
#[derive(Debug, PartialEq, Eq)]
pub struct NeedsCopy<T>(pub T);

impl<T: Copy> Copy for NeedsCopy<T> {}
impl<T: Copy> Clone for NeedsCopy<T> {
    fn clone(&self) -> Self {
        *self
    }
}

pub fn derive_summary() -> String {
    let a = DerivedGeneric { value: 10_i32 };
    let b = a;
    let _eq = a == b;
    let _ord = a.cmp(&b);
    let mut hasher = DefaultHasher::new();
    a.hash(&mut hasher);
    let _hash = hasher.finish();

    let e1 = DerivedEnum::Single(1_i32);
    let e2 = e1.clone();
    let _enum_eq = e1 == e2;

    // Phantom derive vs manual bound contrast: `DerivedPhantom<String>` requires
    // `String: Clone` for derived `Clone`, while `ManualPhantom<String>` clones
    // without that bound.
    let derived_phantom = DerivedPhantom::<String>(PhantomData);
    let derived_phantom_cloned = derived_phantom.clone();
    let manual_phantom = ManualPhantom::<String>::new(5);
    let manual_phantom_cloned = manual_phantom.clone();
    let _phantom_eq = manual_phantom == manual_phantom_cloned;
    let mut hasher2 = DefaultHasher::new();
    manual_phantom.hash(&mut hasher2);
    let _manual_hash = hasher2.finish();
    let _manual_default = ManualPhantom::<String>::default();

    let copy_val = NeedsCopy(3_i32);
    let copy_two = copy_val;
    let _both = copy_val.0 + copy_two.0;

    format!(
        "{a:?}|{e1:?}|{derived_phantom:?}|{manual_phantom:?}|{derived_phantom_cloned:?}|{manual_phantom_cloned:?}|{copy_val:?}"
    )
}
