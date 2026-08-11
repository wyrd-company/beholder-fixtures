// RS-CAN-GEN-004: associated types and constants with defaults, overrides,
// shorthand, and fully qualified projection.

// Trait with associated type and associated constant.
pub trait Record {
    /// Associated type with bound.
    type Key: Clone + std::fmt::Debug;

    /// Associated constant (stable) with default.
    const VERSION: usize = 1;

    /// Additional associated constant without default.
    const LABEL: &'static str;

    fn key(&self) -> Self::Key;
}

// Concrete type using shorthand projection via trait bound.
#[derive(Debug, Clone)]
pub struct Entry {
    pub id: u32,
    pub name: String,
}

impl Record for Entry {
    type Key = u32;
    const LABEL: &'static str = "entry";
    // VERSION uses default 1.

    fn key(&self) -> Self::Key {
        self.id
    }
}

// Type overriding the default constant.
#[derive(Debug, Clone)]
pub struct Archive {
    pub id: u64,
    pub title: String,
}

impl Record for Archive {
    type Key = u64;
    const VERSION: usize = 2;
    const LABEL: &'static str = "archive";

    fn key(&self) -> Self::Key {
        self.id
    }
}

// Trait with associated type default via supertrait? Instead use associated constant
// default demonstration with generic associated type companion; associated type
// defaults remain unstable, so we document that as counterexample and use stable
// constant defaults above.

// Shorthand usage: T::Key referenced through bound.
pub fn print_key<T: Record>(item: &T)
where
    T::Key: std::fmt::Display,
{
    let k = item.key();
    let _ = format!("{k}");
}

// Fully qualified projection: <T as Record>::Key and ::VERSION
pub fn qualified_projection<T: Record>(item: &T) -> (String, usize, &'static str) {
    let k: <T as Record>::Key = item.key();
    let version = <T as Record>::VERSION;
    let label = <T as Record>::LABEL;
    (format!("{k:?}"), version, label)
}

// Constrain equality and bounds on associated types.
pub fn constrained<T, U>(a: T, b: U) -> bool
where
    T: Record<Key = u32>,
    U: Record<Key = u32>,
    T::Key: PartialEq<U::Key>,
{
    a.key() == b.key()
}

// Overriding and distinct associated bindings.
pub fn association_demo() {
    let entry = Entry {
        id: 7,
        name: "demo".to_owned(),
    };
    let archive = Archive {
        id: 99,
        title: "file".to_owned(),
    };
    let _ = print_key(&entry);
    let _ = qualified_projection(&entry);
    let _ = qualified_projection(&archive);
    let another = Entry {
        id: 7,
        name: "other".to_owned(),
    };
    let _eq = constrained(entry, another);
}

// Trait object association note: non-dyn-compatible due to associated constant.
// We show dyn compatibility restriction via separate trait without constants.

// Additional trait demonstrating associated type projection with bound shorthand.
pub trait Transform {
    type Input;
    type Output: Clone;
    fn transform(&self, input: Self::Input) -> Self::Output;
}

pub struct Doubler;

impl Transform for Doubler {
    type Input = u32;
    type Output = u32;
    fn transform(&self, input: Self::Input) -> Self::Output {
        input * 2
    }
}

pub fn use_transform<T: Transform>(t: &T, value: T::Input) -> T::Output
where
    T::Output: std::fmt::Display,
{
    let out = t.transform(value);
    let _ = format!("{out}");
    out
}

// Associated constant with generic context: Self in const expression via
// associated type is not dyn-compatible, but valid for concrete impls.
pub trait SizedRecord: Record
where
    Self: Sized,
{
    fn versioned_key(&self) -> (Self::Key, usize) {
        (self.key(), Self::VERSION)
    }
}

impl SizedRecord for Entry {}
impl SizedRecord for Archive {}

pub fn associated_summary() -> &'static str {
    "associated"
}
