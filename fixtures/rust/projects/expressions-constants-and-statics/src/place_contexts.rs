//! RS-CAN-EXPR-001 — Place, value, and assignee contexts.

use std::ops::{Deref, DerefMut, Index, IndexMut};

/// A wrapper that overloads deref.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Wrapper(pub String);

impl Deref for Wrapper {
    type Target = String;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Wrapper {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

/// A container that overloads indexing by `usize` and `String` key.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IndexedStore {
    pub items: Vec<i32>,
}

impl Index<usize> for IndexedStore {
    type Output = i32;
    fn index(&self, index: usize) -> &Self::Output {
        &self.items[index]
    }
}

impl IndexMut<usize> for IndexedStore {
    fn index_mut(&mut self, index: usize) -> &mut Self::Output {
        &mut self.items[index]
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Record {
    pub field: i32,
    pub label: String,
}

static GLOBAL_COUNTER: std::sync::atomic::AtomicI32 = std::sync::atomic::AtomicI32::new(0);
static GLOBAL_VALUE: i32 = 42;
static PLACE_STATIC_IMMUT: i32 = 123;
static mut PLACE_STATIC_MUT: i32 = 0;

/// Demonstrates locals, statics, dereferences, fields, and indexes
/// in value, borrow, assignment, and compound-assignment contexts.
pub fn demonstrate() -> i32 {
    // Locals in value context (move and copy).
    let local_copy: i32 = 10;
    let moved_string = String::from("harvest");
    let _value_copy = local_copy;
    let _value_moved = moved_string;

    // Borrows.
    let mut record = Record {
        field: 7,
        label: String::from("plot"),
    };
    let _borrow_shared: &i32 = &record.field;
    let _borrow_mut: &mut String = &mut record.label;

    // Parentheses preserving place context: `(&mut x)` remains a place.
    let mut place_holder = 5_i32;
    *(&mut place_holder) = 11;
    (&mut place_holder).clone_from(&12);

    // Dereference place contexts and overloaded Deref.
    let mut wrapped = Wrapper(String::from("field"));
    let _deref_value: char = (*wrapped).chars().next().unwrap_or('?');
    let _deref_borrow: &str = &*wrapped;
    *wrapped = String::from("row");
    // Field through deref.
    let _field_len = wrapped.len();

    // Index contexts: value, borrow, assignment, compound assignment.
    let mut store = IndexedStore {
        items: vec![1, 2, 3],
    };
    let _index_value: i32 = store[1];
    let _index_borrow: &i32 = &store[1];
    let _index_borrow_mut: &mut i32 = &mut store[1];
    store[0] = 10;
    store[1] += 5;
    store[2] *= 2;

    // Field and index combined as assignee.
    record.field = 20;
    record.field += 3;
    record.label.push_str("-amended");

    // Static in value, borrow, assignment, and compound-assignment contexts.
    let _static_value: i32 = GLOBAL_VALUE;
    let _static_borrow: &'static i32 = &GLOBAL_VALUE;
    let _static_immut_value: i32 = PLACE_STATIC_IMMUT;
    let _static_immut_borrow: &'static i32 = &PLACE_STATIC_IMMUT;
    unsafe {
        PLACE_STATIC_MUT = 7;
        PLACE_STATIC_MUT += 4;
        PLACE_STATIC_MUT *= 2;
        let _place_mut_value: i32 = PLACE_STATIC_MUT;
        let _place_mut_borrow: *const i32 = std::ptr::addr_of!(PLACE_STATIC_MUT);
        let _ = _place_mut_borrow;
    }
    GLOBAL_COUNTER.store(7, std::sync::atomic::Ordering::SeqCst);
    GLOBAL_COUNTER.fetch_add(1, std::sync::atomic::Ordering::SeqCst);

    // Different move/copy outcomes: Copy remains valid after assignment, move does not.
    let copy_value: i32 = 99;
    let _first_use = copy_value;
    let _second_use = copy_value; // Copy type reuses.

    let not_copy = String::from("once");
    let _moved_once = not_copy;
    // let _moved_twice = not_copy; // would be invalid move-after-move (documented in counterexamples).

    // Temporary promotion: borrowing a temporary value that would be promotable in const context.
    let _temp_ref: &i32 = &12;

    // Assignment to dereferenced place.
    let mut boxed = Box::new(8_i32);
    *boxed = 20;
    *boxed += 1;

    // Compound assignment on deref/Index/field.
    let mut rec2 = Record {
        field: 2,
        label: String::from("seed"),
    };
    rec2.field *= 4;
    let mut wrap2 = Wrapper(String::from("a"));
    wrap2.push_str("b");

    place_holder + store[0] + rec2.field
}

/// Shows that `=` requires a place; this is the valid counterpart beside a documented invalid case.
#[allow(dead_code)]
fn valid_assignment_targets() {
    let mut x = 0;
    x = 1;
    let mut rec = Record {
        field: 0,
        label: String::new(),
    };
    rec.field = 2;
    let mut boxed = Box::new(3);
    *boxed = 4;
    let mut arr = [0; 3];
    arr[0] = 5;
    let mut store = IndexedStore { items: vec![0] };
    store[0] = 6;
}
