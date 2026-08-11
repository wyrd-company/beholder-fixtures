//! RS-CAN-TYPE-001 — struct forms, construction, update, and destructuring.

use std::marker::PhantomData;

// Named-field struct.
#[derive(Debug, Clone, PartialEq)]
pub struct Named {
    pub x: i32,
    pub y: String,
}

// Tuple struct.
#[derive(Debug, Clone, PartialEq)]
pub struct Tuple(pub i32, pub String);

// Unit struct.
#[derive(Debug, Clone, PartialEq, Default)]
pub struct Unit;

// Zero-field braced struct (distinct from unit syntax).
#[derive(Debug, Clone, PartialEq, Default)]
pub struct Empty {}

// Small zero-sized struct.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Marker;

// Generic struct with a default type parameter.
#[derive(Debug, Clone, PartialEq)]
pub struct GenericWithDefault<T = i32> {
    pub value: T,
    pub label: String,
}

// Copy-only fields to demonstrate copying the remaining field.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct CopyFields {
    pub a: i32,
    pub b: u32,
}

// Phantom-bearing struct changes variance without storage.
#[derive(Debug)]
pub struct WithPhantom<T> {
    pub id: u32,
    pub marker: PhantomData<T>,
}

pub fn named_example() -> Named {
    Named {
        x: 10,
        y: "harvest".to_string(),
    }
}

pub fn tuple_example() -> Tuple {
    Tuple(4, "field".to_string())
}

pub fn unit_example() -> Unit {
    Unit
}

pub fn empty_example() -> Empty {
    Empty {}
}

pub fn construction_examples() -> (Named, Tuple, Unit, Empty) {
    let named = Named {
        x: 1,
        y: "plot".to_string(),
    };
    let tuple = Tuple(2, "row".to_string());
    let unit = Unit;
    let empty = Empty {};
    (named, tuple, unit, empty)
}

pub fn update_examples() {
    let original = Named {
        x: 1,
        y: "soil".to_string(),
    };
    // Update moving the remaining non-Copy field: `y: String` is moved, `x: i32` is copied.
    let updated = Named { x: 9, ..original };
    assert_eq!(updated.x, 9);
    assert_eq!(updated.y, "soil");

    // Remaining Copy field is copied: both `a` and `b` are Copy.
    let base_copy = CopyFields { a: 1, b: 2 };
    let copied = CopyFields { a: 9, ..base_copy };
    assert_eq!(copied.a, 9);
    assert_eq!(copied.b, 2);
    // `base_copy` remains usable because `b` was copied.
    assert_eq!(base_copy.b, 2);

    // Update with tuple struct via struct update through deconstruction.
    let first = Tuple(1, "alpha".to_string());
    let second = Tuple(first.0 + 1, first.1.clone());
    let _ = second;
}

pub fn destructure_examples() {
    let named = Named {
        x: 3,
        y: "seed".to_string(),
    };
    let Named { x, y } = named;
    let _ = (x, y);

    let tuple = Tuple(8, "bundle".to_string());
    let Tuple(a, b) = tuple;
    let _ = (a, b);

    let empty = Empty {};
    let Empty {} = empty;

    let unit = Unit;
    let Unit = unit;

    // Pattern match with update binding.
    #[allow(clippy::match_single_binding)]
    {
        let sample = Named {
            x: 5,
            y: "canopy".to_string(),
        };
        match sample {
            Named { x, .. } => {
                let _ = x;
            }
        }
    }
}

pub fn constructor_as_value() {
    // Tuple constructor can be used as a function value.
    let maker: fn(i32, String) -> Tuple = Tuple;
    let built = maker(3, "cutting".to_string());
    assert_eq!(built.0, 3);

    // Unit-struct value is its own constructor.
    let make_unit: fn() -> Unit = || Unit;
    let _ = make_unit();
}

pub fn zst_and_phantom() {
    assert_eq!(std::mem::size_of::<Marker>(), 0);
    assert_eq!(std::mem::size_of::<Empty>(), 0);
    assert_eq!(std::mem::size_of::<Unit>(), 0);

    let with = WithPhantom::<String> {
        id: 12,
        marker: PhantomData,
    };
    let _ = with.id;

    // Zero-sized generics still participate in type identity.
    let gen_default: GenericWithDefault = GenericWithDefault {
        value: 1,
        label: "a".to_string(),
    };
    let gen_explicit: GenericWithDefault<String> = GenericWithDefault {
        value: "explicit".to_string(),
        label: "b".to_string(),
    };
    let _ = (gen_default, gen_explicit);
}

pub fn cross_crate_visibility() {
    // Private-field external construction is documented in counterexamples;
    // here we construct through the public constructor from the downstream crate.
    let from_downstream = types_layout_downstream::PrivateFields::new(3, "hidden".to_string());
    assert_eq!(from_downstream.public, 3);
    assert_eq!(from_downstream.private(), "hidden");

    // Non-exhaustive struct must be constructed via its constructor.
    let record = types_layout_downstream::ExternalRecord::new(10, 20);
    assert_eq!(record.visible, 10);
    assert_eq!(record.hidden(), 20);
}
