//! RS-CAN-TRAIT-010 — operator, index, deref, and formatting traits invoked only through syntax.

use std::ops::{Add, AddAssign, Deref, DerefMut, Index, IndexMut};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Count(pub i32);

impl Add for Count {
    type Output = Count;
    fn add(self, rhs: Self) -> Self::Output {
        Count(self.0 + rhs.0)
    }
}

impl AddAssign for Count {
    fn add_assign(&mut self, rhs: Self) {
        self.0 += rhs.0;
    }
}

impl PartialOrd for Count {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Count {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.0.cmp(&other.0)
    }
}

/// Wrapper for indexing and deref.
pub struct Buffer(pub Vec<i32>);

impl Index<usize> for Buffer {
    type Output = i32;
    fn index(&self, index: usize) -> &Self::Output {
        &self.0[index]
    }
}

impl IndexMut<usize> for Buffer {
    fn index_mut(&mut self, index: usize) -> &mut Self::Output {
        &mut self.0[index]
    }
}

impl Deref for Buffer {
    type Target = [i32];
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Buffer {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[derive(Debug)]
pub struct Displayed(pub i32);

impl std::fmt::Display for Displayed {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Displayed({})", self.0)
    }
}

pub fn operator_summary() -> String {
    // Arithmetic via syntax only (no direct trait method call).
    let a = Count(2);
    let b = Count(3);
    let c = a + b;
    let mut d = Count(1);
    d += Count(4);

    // Comparison via syntax.
    let eq = a == Count(2);
    let lt = a < b;

    // Indexing via syntax.
    let mut buf = Buffer(vec![10, 20, 30]);
    let first = buf[0];
    buf[1] = 99;
    // Deref coercion via syntax: Buffer derefs to [i32], so slice methods usable.
    let len = buf.len();
    let slice_sum: i32 = buf.iter().sum();

    // Formatting via syntax.
    let displayed = Displayed(42);
    let formatted = format!("{displayed}");
    let debug = format!("{c:?}");

    format!(
        "{c:?}|{d:?}|{eq}|{lt}|{first}|{}|{len}|{slice_sum}|{formatted}|{debug}",
        buf[1]
    )
}
