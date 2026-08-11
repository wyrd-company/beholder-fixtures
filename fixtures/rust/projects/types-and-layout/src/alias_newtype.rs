//! RS-CAN-TYPE-004 — type alias versus nominal newtype.

use std::fmt;

// Type alias is another path to the same type.
pub type Alias = Vec<String>;

// Nominal newtype over the same representation.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Newtype(pub Vec<String>);

// Generic alias.
pub type GenericAlias<T> = Vec<T>;

// Trait-object alias.
pub type DisplayBox = Box<dyn fmt::Display>;

// Associated alias example.
pub trait Container {
    type Item;
    type Alias: IntoIterator<Item = Self::Item>;
}

pub struct StringContainer;

impl Container for StringContainer {
    type Item = String;
    type Alias = Alias;
}

// Inherent impl written through alias belongs to the underlying type.
// Demonstrated by implementing a trait on the underlying local type via an
// alias path where legal. Here we add an inherent helper for Alias-like use.
pub trait Described {
    fn describe(&self) -> String;
}

impl Described for Vec<String> {
    fn describe(&self) -> String {
        format!("alias with {} items", self.len())
    }
}

// Alias-backed impl: this `impl` header uses a local type reachable through
// the alias name; it still establishes an impl for `Vec<String>`.
impl StringContainer {
    pub fn via_alias(values: Alias) -> Newtype {
        Newtype(values)
    }
}

impl Newtype {
    pub fn new(values: Vec<String>) -> Self {
        Self(values)
    }

    pub fn inner(&self) -> &[String] {
        &self.0
    }

    pub fn describe(&self) -> String {
        format!("newtype with {} items", self.0.len())
    }
}

pub fn alias_coherence_and_methods() -> (String, String) {
    let alias_values: Alias = vec!["field".to_string(), "meadow".to_string()];
    let newtype_values = Newtype(vec!["field".to_string(), "meadow".to_string()]);

    // Coercion/assignment: alias is the same type, newtype is not.
    let via_alias: Vec<String> = alias_values.clone();
    let _ = via_alias.describe();

    // Newtype requires explicit wrapping.
    let desc_alias = alias_values.describe();
    let desc_newtype = newtype_values.describe();

    (desc_alias, desc_newtype)
}

pub fn alias_constructor_path() {
    // Alias has no constructor of its own; construction uses the underlying
    // type path.
    let alias_vec: Alias = Vec::new();
    let explicit: Vec<String> = Vec::new();
    let _ = (alias_vec, explicit);

    // Trait-object alias construction.
    let boxed: DisplayBox = Box::new(42_i32);
    let _ = boxed.to_string();
}

pub fn generic_alias_variants() {
    let a: GenericAlias<u32> = vec![1, 2, 3];
    let b: GenericAlias<String> = vec!["plot".to_string()];
    let _ = (a, b);
}
