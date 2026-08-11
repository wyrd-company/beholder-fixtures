//! RS-CAN-OWN-008: Pattern binding modes and match ergonomics (edition 2024 view).
//! Paired edition 2021 behavior lives in `crates/edition-2021`.

pub struct Container {
    pub value: String,
    pub count: u32,
}

/// Match one structure as owned, shared, and mutable reference with inferred binding modes.
/// Edition 2024 inferred mode: `match &container` automatically binds fields as references.
pub fn inferred_binding_modes() -> (String, u32, String) {
    // Owned scrutinee: fields moved/copied.
    let owned = Container {
        value: String::from("owned"),
        count: 1,
    };
    let (moved_value, copied_count) = match owned {
        Container { value, count } => (value, count),
    };

    // Shared reference scrutinee with inferred mode: fields borrowed.
    let shared = Container {
        value: String::from("shared"),
        count: 2,
    };
    let (shared_len, _shared_count) = match &shared {
        Container { value, count } => (value.len(), *count),
    };
    let _ = shared_len;

    // Mutable reference scrutinee with inferred mode.
    let mut m = Container {
        value: String::from("mut"),
        count: 3,
    };
    match &mut m {
        Container { value, count } => {
            value.push_str("!");
            *count += 1;
        }
    }

    (moved_value, copied_count, m.value)
}

/// Explicit binding modes in edition 2024. Unlike the inferred match ergonomics
/// above, every binding here is written explicitly: `ref`/`mut` on an owned
/// scrutinee (default mode by-value), and leading `&`/`&mut` reference patterns
/// that *reset* the default binding mode when matching shared and mutable
/// references. Explicit `ref` directly under an inherited `&` mode is rejected
/// in 2024 (see `docs/counterexamples.md`); the leading reference pattern is
/// what makes the explicit inner bindings legal.
pub fn explicit_binding_modes_2024() -> (String, u32) {
    // Owned scrutinee, explicit `ref`: bindings are `&String` / `&u32` even
    // though the default binding mode on an owned scrutinee is by-value.
    let container = Container {
        value: String::from("explicit"),
        count: 5,
    };
    let len = match container {
        Container {
            ref value,
            ref count,
        } => value.len() + *count as usize,
    };

    // Owned scrutinee, explicit `mut` binding.
    let owned = Container {
        value: String::from("mut-binding"),
        count: 0,
    };
    let (value, _count) = match owned {
        Container { mut value, count } => {
            value.push_str("-modified");
            (value, count)
        }
    };

    // Shared reference scrutinee matched with a leading `&` reference pattern.
    // The `&` resets the default binding mode to by-value, so `ref value` is an
    // explicit reference binding (`&String`, since a `String` cannot move out of
    // a shared borrow) and the `Copy` `count` binds by value.
    let shared = Container {
        value: String::from("shared-ref"),
        count: 7,
    };
    let shared_len = match &shared {
        &Container { ref value, count } => value.len() + count as usize,
    };

    // Mutable reference scrutinee matched with a leading `&mut` reference
    // pattern that resets the binding mode; `ref mut` then binds each field by
    // unique reference (`&mut String` / `&mut u32`).
    let mut m = Container {
        value: String::from("mut-ref"),
        count: 1,
    };
    match &mut m {
        &mut Container {
            ref mut value,
            ref mut count,
        } => {
            value.push_str("!");
            *count += 1;
        }
    }

    (value, (len + shared_len + m.count as usize) as u32)
}

/// `@` bindings and nested references remain valid.
pub fn at_and_nested_reference() -> String {
    let container = Container {
        value: String::from("at-binding"),
        count: 10,
    };
    match &container {
        Container {
            value: v @ _,
            count,
        } if *count > 5 => v.clone(),
        _ => String::new(),
    }
}

/// Or-pattern agreement: both arms bind same names with same types.
pub fn or_pattern_agreement(container: &Container) -> String {
    match container {
        Container { value, count: 1 } | Container { value, count: 2 } => value.clone(),
        Container { value, .. } => value.clone(),
    }
}

pub fn binding_modes_summary() -> (String, u32, String, String) {
    let (a, b, c) = inferred_binding_modes();
    let (d, _) = explicit_binding_modes_2024();
    let e = at_and_nested_reference();
    let _ = or_pattern_agreement(&Container {
        value: String::from("or"),
        count: 1,
    });
    let _ = e.len();
    (a, b, c, d)
}
