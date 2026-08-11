// RS-CAN-GEN-005: lifetime-parameterized generic associated type
// with required where Self: 'a and a generic consumer.

// Lending-style trait with GAT.
pub trait Lending {
    type Item<'a>
    where
        Self: 'a;

    fn get(&self) -> Self::Item<'_>;
    fn get_for<'a>(&'a self) -> Self::Item<'a>
    where
        Self: 'a;
}

// Concrete type with borrowed slice.
#[derive(Debug, Clone)]
pub struct Store {
    pub data: Vec<String>,
}

impl Lending for Store {
    type Item<'a>
        = &'a str
    where
        Self: 'a;

    fn get(&self) -> Self::Item<'_> {
        self.data.first().map(String::as_str).unwrap_or("")
    }

    fn get_for<'a>(&'a self) -> Self::Item<'a>
    where
        Self: 'a,
    {
        self.get()
    }
}

// Second impl with owned container borrowed as slice.
#[derive(Debug)]
pub struct Buffer {
    pub bytes: Vec<u8>,
}

impl Lending for Buffer {
    type Item<'a>
        = &'a [u8]
    where
        Self: 'a;

    fn get(&self) -> Self::Item<'_> {
        &self.bytes
    }

    fn get_for<'a>(&'a self) -> Self::Item<'a>
    where
        Self: 'a,
    {
        &self.bytes
    }
}

// Generic consumer over GAT.
pub fn consume_lending<T: Lending>(item: &T) -> String
where
    for<'a> T::Item<'a>: AsRef<str>,
    // Alternatively, direct display via borrowed form.
{
    let borrowed = item.get();
    // We require AsRef<str> to demonstrate projection bound.
    borrowed.as_ref().to_owned()
}

// Consumer demonstrating higher-ranked projection bound on GAT.
pub fn count_chars<T>(store: &T) -> usize
where
    T: Lending,
    for<'a> T::Item<'a>: AsRef<str>,
{
    store.get().as_ref().len()
}

// Consumer returning borrowed item directly (lifetime tied to input).
pub fn borrow_item<'a, T>(store: &'a T) -> T::Item<'a>
where
    T: Lending,
    T: 'a,
{
    store.get_for::<'a>()
}

// Additional GAT with type parameter (demonstrates type-parameterized GAT
// alongside lifetime; still requires Self: 'a for borrow).
pub trait Mapping {
    type View<'a, T>
    where
        Self: 'a,
        T: 'a;

    fn view<'a, T>(&'a self, value: &'a T) -> Self::View<'a, T>
    where
        Self: 'a;
}

pub struct IdentityMap;

impl Mapping for IdentityMap {
    type View<'a, T>
        = &'a T
    where
        Self: 'a,
        T: 'a;

    fn view<'a, T>(&'a self, value: &'a T) -> Self::View<'a, T>
    where
        Self: 'a,
    {
        value
    }
}

pub fn gat_summary() -> &'static str {
    "gat"
}
