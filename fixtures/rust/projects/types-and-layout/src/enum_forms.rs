//! RS-CAN-TYPE-002 — enum variant forms, discriminants, fieldless casts, and cross-crate non-exhaustiveness.

use types_layout_downstream::ExternalChoice;

// All enum variant forms.
#[derive(Debug, Clone, PartialEq)]
pub enum Shaped {
    Unit,
    Tuple(i32, String),
    Struct { x: i32, label: String },
}

// Explicit and computed discriminants.
#[repr(i32)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Discriminated {
    Alpha = 2,
    Beta = 5,
    Gamma, // computed as 6 from preceding Beta
}

// Fieldless enum suitable for `as` casts.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Fieldless {
    Red = 1,
    Green = 2,
    Blue = 3,
}

// Integer-repr variant set used for discriminant observation.
#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ByteRepr {
    A = 0x10,
    B = 0x20,
    C = 0x30,
}

// Conditional variant demonstration.
#[derive(Debug, Clone, PartialEq)]
pub enum WithConditional {
    Present(i32),
    #[cfg(fixture_highlight)]
    Highlighted(String),
    Fallback,
}

pub fn construction_and_import() {
    // Direct construction of each variant form.
    let u = Shaped::Unit;
    let t = Shaped::Tuple(7, "parcel".to_string());
    let s = Shaped::Struct {
        x: 3,
        label: "meadow".to_string(),
    };
    let _ = (u, t, s);

    // Imported variant names.
    use Shaped::{Struct, Tuple, Unit as ShapedUnit};
    let _ = ShapedUnit;
    let _ = Tuple(1, "imported".to_string());
    let _ = Struct {
        x: 0,
        label: "imported".to_string(),
    };

    // Constructor as function: tuple variant coerces to function pointer.
    let maker: fn(i32, String) -> Shaped = Shaped::Tuple;
    let _ = maker(2, "as_fn".to_string());

    // Self::Variant inside impl.
    assert_eq!(Shaped::unit_label(), "unit");
}

impl Shaped {
    pub fn unit_label() -> &'static str {
        match Self::Unit {
            Self::Unit => "unit",
            _ => "other",
        }
    }
}

pub fn discriminant_observation() -> (i32, u8) {
    // Fieldless `as` casts.
    let red = Fieldless::Red as i32;
    let blue = Fieldless::Blue as u8;
    assert_eq!(red, 1);
    assert_eq!(blue, 3);

    // Repr-backed discriminant retrieval.
    let val = Discriminated::Beta as i32;
    assert_eq!(val, 5);

    // Discriminant via explicit cast on byte repr.
    let byte = ByteRepr::B as u8;
    assert_eq!(byte, 0x20);

    (val, byte)
}

pub fn exhaustive_matching(example: Shaped) -> &'static str {
    match example {
        Shaped::Unit => "unit",
        Shaped::Tuple(_, _) => "tuple",
        Shaped::Struct { .. } => "struct",
    }
}

pub fn cross_crate_exhaustive(choice: ExternalChoice) -> &'static str {
    // Cross-crate non_exhaustive requires a wildcard arm.
    match choice {
        ExternalChoice::Alpha => "alpha",
        ExternalChoice::Beta => "beta",
        _ => "other",
    }
}

pub fn downstream_match_wildcard_is_required() -> bool {
    // Demonstrate that downstream enum is non_exhaustive by forcing wildcard
    // usage; absolute matching without wildcard would fail to compile when a new
    // downstream variant is added.
    let value = ExternalChoice::Gamma;
    !matches!(value, ExternalChoice::Alpha | ExternalChoice::Beta)
}

pub fn fieldless_casts() -> (isize, isize) {
    let a = Fieldless::Green as isize;
    let b = ByteRepr::C as isize;
    (a, b)
}
