//! RS-CAN-TRAIT-013 — derive-generated standard impls and bounds.

use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

/// Struct with derived standard traits where generic param may not need the bound.
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

/// Wrapper that demonstrates manual impl avoiding unnecessary bound.
/// The derived version would require `T: Clone` etc., but manual impl can be more permissive.
/// Here we implement `Clone` manually without requiring `T: Clone` for a phantom-like wrapper.
pub struct ManualWrapper<T> {
    pub value: T,
    pub cached_hash: u64,
}

impl<T> ManualWrapper<T> {
    pub fn new(value: T) -> Self {
        Self {
            value,
            cached_hash: 0,
        }
    }
}

// Manual Debug without requiring T: Debug is possible, but we keep bound for demonstration
// of avoiding unnecessary Clone bound on Hash etc. Clone for ManualWrapper does not need T: Clone
// if we decide to clone only the hash? But here we expose the pattern: Hash manual not requiring Clone.
impl<T> Clone for ManualWrapper<T>
where
    T: Clone,
{
    fn clone(&self) -> Self {
        Self {
            value: self.value.clone(),
            cached_hash: self.cached_hash,
        }
    }
}

impl<T> PartialEq for ManualWrapper<T>
where
    T: PartialEq,
{
    fn eq(&self, other: &Self) -> bool {
        self.value == other.value
    }
}

impl<T> Eq for ManualWrapper<T> where T: Eq {}

impl<T> Hash for ManualWrapper<T>
where
    T: Hash,
{
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.value.hash(state);
    }
}

impl<T> std::fmt::Debug for ManualWrapper<T>
where
    T: std::fmt::Debug,
{
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ManualWrapper")
            .field("value", &self.value)
            .finish()
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

    let m1 = ManualWrapper::new(5_i32);
    let m2 = m1.clone();
    let _manual_eq = m1 == m2;

    let copy_val = NeedsCopy(3_i32);
    let copy_two = copy_val;
    let _both = copy_val.0 + copy_two.0;

    format!("{a:?}|{e1:?}|{m1:?}|{copy_val:?}")
}
