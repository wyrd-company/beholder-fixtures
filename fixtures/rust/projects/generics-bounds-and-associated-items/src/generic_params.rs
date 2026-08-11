use std::collections::HashMap;
use std::marker::PhantomData;

// RS-CAN-GEN-001: structs, enums, functions, traits, impls, aliases, associated items
// using lifetime, type, and const parameters with legal defaults.

/// Container demonstrating lifetime, type, and const defaults on a struct.
#[derive(Debug, Clone)]
pub struct Inventory<'a, T = String, const N: usize = 4>
where
    T: Clone + Default,
{
    pub label: &'a str,
    pub items: [T; N],
    pub marker: PhantomData<&'a T>,
}

impl<'a, T, const N: usize> Inventory<'a, T, N>
where
    T: Clone + Default,
{
    pub fn new(label: &'a str) -> Self {
        Self {
            label,
            items: std::array::from_fn(|_| T::default()),
            marker: PhantomData,
        }
    }

    pub fn len(&self) -> usize {
        N
    }
}

/// Enum with lifetime, type, and const defaults.
#[derive(Debug)]
pub enum Tagged<'a, T = u32, const FLAG: bool = true> {
    Borrowed(&'a T),
    Owned(T),
    Empty,
}

/// Trait with lifetime, type, and const defaults.
pub trait Repository<'a, T = String, const LIMIT: usize = 10> {
    type Item;
    fn store(&'a mut self, item: Self::Item) -> Option<T>;
    fn capacity() -> usize {
        LIMIT
    }
}

/// Type alias with defaults demonstrating ordering and defaults.
pub type DefaultMap<K = String, V = u32> = HashMap<K, V>;

/// Alias to struct using defaults (demonstrates inferred defaults).
pub type DefaultInventory<'a> = Inventory<'a>;

/// Free function with lifetime, type, and const parameters (legal: no defaults on function).
pub fn process<'a, T, const N: usize>(input: &'a [T; N]) -> &'a T
where
    T: Clone,
{
    &input[0]
}

/// Function showing inferred defaults at call site.
pub fn inferred_defaults_demo() {
    let inv: Inventory<'static> = Inventory::<'static, String, 4>::new("demo");
    let _ = inv.len();
    let _map: DefaultMap = HashMap::new();
}

/// Trait impl demonstrating generic parameters on impl block.
impl<'a> Repository<'a> for Inventory<'a, String, 4> {
    type Item = String;
    fn store(&'a mut self, item: Self::Item) -> Option<String> {
        let _ = item;
        None
    }
}

/// Associated item with own generics: trait with generic method carrying lifetime/type/const.
pub trait Converter {
    fn convert<'a, T, const N: usize>(&'a self, input: &'a [T; N]) -> Vec<T>
    where
        T: Clone + 'a;
}

impl Converter for Inventory<'_, String, 2> {
    fn convert<'a, T, const N: usize>(&'a self, input: &'a [T; N]) -> Vec<T>
    where
        T: Clone + 'a,
    {
        input.to_vec()
    }
}

/// Demonstrates unused type parameter via PhantomData.
#[derive(Debug)]
pub struct Unused<T> {
    _marker: PhantomData<T>,
}

impl<T> Unused<T> {
    #[allow(clippy::new_without_default)]
    pub fn new() -> Self {
        Self {
            _marker: PhantomData,
        }
    }
}

/// Early-bound lifetime (struct) vs late-bound lifetime (function) contrast.
pub struct Early<'a> {
    pub reference: &'a u32,
}

/// Late-bound lifetime appears only in function signature.
#[allow(clippy::needless_lifetimes)]
pub fn late_bound<'a>(value: &'a u32) -> &'a u32 {
    value
}

/// Parameter shadowing: outer T shadowed by inner generic.
pub struct Outer<T> {
    pub value: T,
}

impl<T> Outer<T> {
    pub fn inner<U>(&self, other: U) -> U
    where
        U: Clone,
    {
        other.clone()
    }

    // Inner function generic shadows outer impl generic name.
    pub fn shadowed<V>(&self, value: V) -> V {
        value
    }
}

/// Demonstrates ordering: lifetime before type before const.
pub struct Ordered<'a, T, const N: usize> {
    pub reference: &'a T,
    pub array: [T; N],
}

impl<'a, T, const N: usize> Ordered<'a, T, N>
where
    T: Clone + Default,
{
    pub fn describe(&self) -> usize {
        N
    }
}

/// Alias with lifetime, type, and const defaults.
pub type LifetimeAlias<'a, T = &'a str, const N: usize = 4> = Ordered<'a, T, N>;

/// Alias with type and const defaults using array.
pub type ArrayAlias<T = u8, const N: usize = 4> = [T; N];

/// Type alias demonstrating default inference and explicit override.
pub fn alias_usage() {
    let _a: DefaultInventory<'static> = Inventory::new("alias");
    let _b: Inventory<'static, String, 8> = Inventory::new("explicit");
    let _c: LifetimeAlias<'static> = Ordered {
        reference: &"aliased",
        array: ["aliased"; 4],
    };
    let _d: ArrayAlias = [0u8; 4];
    let _e: ArrayAlias<u32, 2> = [1u32; 2];
}

/// Module demonstrating scope of generic parameters.
pub mod scope_demo {
    use super::PhantomData;

    pub struct ScopeOuter<T> {
        pub phantom: PhantomData<T>,
    }

    impl<T> ScopeOuter<T> {
        pub fn method<U>(&self, input: U) -> (PhantomData<T>, U) {
            (PhantomData, input)
        }
    }
}

pub fn generic_params_summary() -> &'static str {
    "generic_params"
}
