//! RS-CAN-TYPE-009 — dyn-compatible trait objects, bindings, upcasting.

use std::fmt::Debug;

// Dyn-compatible base trait.
pub trait Draw: Debug {
    fn render(&self) -> String;
    fn label(&self) -> &str;
}

// Trait with associated type binding.
pub trait Container: Debug {
    type Item: Debug;
    fn item(&self) -> &Self::Item;
}

// Trait with lifetime parameter.
pub trait Borrowed<'a>: Debug {
    fn view(&self) -> &'a str;
}

// Auto-trait set demonstration: Send + Sync become part of object identity.
pub trait DisplayHint: Debug + Send + Sync {
    fn hint(&self) -> &'static str;
}

#[derive(Debug)]
pub struct Circle {
    pub radius: f64,
    pub label: String,
}

#[derive(Debug)]
pub struct Square {
    pub side: f64,
    pub label: String,
}

impl Draw for Circle {
    fn render(&self) -> String {
        format!("circle {}", self.radius)
    }
    fn label(&self) -> &str {
        &self.label
    }
}

impl Draw for Square {
    fn render(&self) -> String {
        format!("square {}", self.side)
    }
    fn label(&self) -> &str {
        &self.label
    }
}

#[derive(Debug)]
pub struct StringContainer(pub String);

impl Container for StringContainer {
    type Item = String;
    fn item(&self) -> &String {
        &self.0
    }
}

#[derive(Debug)]
pub struct BorrowedView<'a> {
    pub text: &'a str,
}

impl<'a> Borrowed<'a> for BorrowedView<'a> {
    fn view(&self) -> &'a str {
        self.text
    }
}

#[derive(Debug)]
pub struct Hinted(pub &'static str);

impl DisplayHint for Hinted {
    fn hint(&self) -> &'static str {
        self.0
    }
}

// Trait with an incompatible method repaired by `Self: Sized`.
pub trait MaybeDyn {
    fn only_sized(&self) -> i32
    where
        Self: Sized;

    fn dyn_safe(&self) -> &'static str;
}

#[derive(Debug)]
pub struct Repaired;

impl MaybeDyn for Repaired {
    fn only_sized(&self) -> i32 {
        7
    }
    fn dyn_safe(&self) -> &'static str {
        "dyn_safe"
    }
}

// Upcasting hierarchy (Rust 1.86+).
pub trait Animal: Debug {
    fn name(&self) -> &'static str;
}

pub trait Pet: Animal {
    fn kind(&self) -> &'static str;
}

#[derive(Debug)]
pub struct Dog;

impl Animal for Dog {
    fn name(&self) -> &'static str {
        "dog"
    }
}

impl Pet for Dog {
    fn kind(&self) -> &'static str {
        "pet dog"
    }
}

pub fn trait_object_bindings() {
    // Dyn trait with associated type binding.
    let container: Box<dyn Container<Item = String>> =
        Box::new(StringContainer("meadow".to_string()));
    assert_eq!(container.item(), "meadow");

    // Dyn trait with lifetime binding.
    let text = "plot".to_string();
    let borrowed: Box<dyn Borrowed<'_>> = Box::new(BorrowedView { text: &text });
    assert_eq!(borrowed.view(), "plot");

    // Dyn trait with auto-trait binding.
    let hinted: Box<dyn DisplayHint> = Box::new(Hinted("hint"));
    assert_eq!(hinted.hint(), "hint");

    // Heterogeneous collection of trait objects.
    let items: Vec<Box<dyn Draw>> = vec![
        Box::new(Circle {
            radius: 3.0,
            label: "c".to_string(),
        }),
        Box::new(Square {
            side: 4.0,
            label: "s".to_string(),
        }),
    ];
    assert_eq!(items.len(), 2);
}

pub fn repaired_dyn_compatible() {
    let obj: Box<dyn MaybeDyn> = Box::new(Repaired);
    assert_eq!(obj.dyn_safe(), "dyn_safe");
    // `only_sized` cannot be called through `dyn MaybeDyn`.
}

pub fn upcasting_demo() {
    let pet: Box<dyn Pet> = Box::new(Dog);
    // Trait upcasting: Box<dyn Pet> coerces to Box<dyn Animal>.
    let animal: Box<dyn Animal> = pet;
    assert_eq!(animal.name(), "dog");

    let pet_ref: &dyn Pet = &Dog;
    let animal_ref: &dyn Animal = pet_ref;
    assert_eq!(animal_ref.name(), "dog");
}
