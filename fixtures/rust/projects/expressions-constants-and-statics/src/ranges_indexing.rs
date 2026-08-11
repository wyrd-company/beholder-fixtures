//! RS-CAN-EXPR-007 — Ranges, indexing, and slicing.

use std::ops::{
    Index, IndexMut, Range, RangeFrom, RangeFull, RangeInclusive, RangeTo, RangeToInclusive,
};

/// Custom indexing type demonstrating user `Index`/`IndexMut`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Grid {
    data: Vec<i32>,
    cols: usize,
}

impl Grid {
    pub fn new(rows: usize, cols: usize) -> Self {
        Self {
            data: vec![0; rows * cols],
            cols,
        }
    }

    pub fn set(&mut self, row: usize, col: usize, value: i32) {
        self.data[row * self.cols + col] = value;
    }
}

impl Index<usize> for Grid {
    type Output = [i32];
    fn index(&self, index: usize) -> &Self::Output {
        let start = index * self.cols;
        &self.data[start..start + self.cols]
    }
}

impl IndexMut<usize> for Grid {
    fn index_mut(&mut self, index: usize) -> &mut Self::Output {
        let start = index * self.cols;
        &mut self.data[start..start + self.cols]
    }
}

/// Exercise every range form as values.
pub fn range_forms() {
    let _full: RangeFull = ..;
    let _from: RangeFrom<i32> = 2..;
    let _to: RangeTo<i32> = ..5;
    let _range: Range<i32> = 1..5;
    let _inclusive: RangeInclusive<i32> = 1..=5;
    let _to_inclusive: RangeToInclusive<i32> = ..=5;

    // Iteration over inclusive edge.
    let collected: Vec<i32> = (1..=3).collect();
    assert_eq!(collected, vec![1, 2, 3]);

    // Empty range.
    let empty: Vec<i32> = (5..5).collect();
    assert!(empty.is_empty());

    // Range expressions used for slicing below.
}

/// Range patterns (allowed integer and char intervals in `match`).
pub fn range_patterns(value: i32, ch: char) -> (&'static str, &'static str) {
    let int_label = match value {
        0..=9 => "digit",
        10..=99 => "two-digit",
        _ => "other",
    };

    let char_label = match ch {
        'a'..='z' => "lower",
        'A'..='Z' => "upper",
        '0'..='9' => "digit-char",
        _ => "other",
    };

    (int_label, char_label)
}

/// Built-in indexing and slicing.
pub fn builtin_index_and_slice() -> i32 {
    let arr = [10, 20, 30, 40, 50];
    let _first = arr[0];
    let _slice: &[i32] = &arr[1..4];
    let _inclusive_slice: &[i32] = &arr[1..=3];
    let _from_slice: &[i32] = &arr[2..];
    let _to_slice: &[i32] = &arr[..3];

    // Mutable indexing.
    let mut vec = vec![1, 2, 3, 4, 5];
    vec[1] = 20;
    vec[2..4].copy_from_slice(&[30, 40]);
    vec[0] += 5;

    // String slicing by range (byte indices, must be on valid UTF-8 boundaries).
    let text = String::from("harvest field");
    let _prefix: &str = &text[0..7];
    let _suffix: &str = &text[8..];

    // Runtime bounds are enforced; unconditional-panic lint would fire for compile-time out-of-bounds literal index
    // (documented in counterexamples, not executed here).

    vec[0] + _first
}

/// User-defined mutable indexing.
pub fn user_mutable_indexing() -> i32 {
    let mut grid = Grid::new(2, 3);
    grid.set(0, 0, 1);
    grid.set(0, 1, 2);
    grid.set(1, 2, 9);

    // Immutable index.
    let row0: &[i32] = &grid[0];
    let sum0: i32 = row0.iter().sum();

    // Mutable index.
    grid[1][0] = 7;
    grid[1][1] += 3;

    sum0 + grid[1][0]
}

/// Range slicing with user type that supports slicing via prior Index impl.
/// Also demonstrates explicit unsafe unchecked alternative.
pub fn range_slicing_and_unchecked() -> i32 {
    let data = vec![10, 20, 30, 40, 50, 60];
    let _s1: &[i32] = &data[1..4];
    let _s2: &[i32] = &data[..=2];
    let _s3: &[i32] = &data[3..];
    let _s4: &[i32] = &data[..3];

    // Unsafe unchecked indexing alternative: caller ensures bounds are correct.
    let value = unsafe { *data.get_unchecked(2) };
    value
}

pub fn demonstrate() -> i32 {
    range_forms();
    let _ = range_patterns(42, 'a');
    let _ = builtin_index_and_slice();
    let _ = user_mutable_indexing();
    let _ = range_slicing_and_unchecked();
    1
}
