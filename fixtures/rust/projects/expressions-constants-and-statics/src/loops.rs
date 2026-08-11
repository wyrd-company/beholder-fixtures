//! RS-CAN-EXPR-004 — Loops, labels, iteration, and value-bearing break.

use std::collections::VecDeque;

/// Custom iterator: owned collection and its iterator.
pub struct RowCollection(pub Vec<String>);

impl RowCollection {
    pub fn new(items: Vec<String>) -> Self {
        Self(items)
    }
}

pub struct RowIter {
    items: Vec<String>,
    index: usize,
}

impl Iterator for RowIter {
    type Item = String;
    fn next(&mut self) -> Option<Self::Item> {
        if self.index < self.items.len() {
            let val = self.items[self.index].clone();
            self.index += 1;
            Some(val)
        } else {
            None
        }
    }
}

impl IntoIterator for RowCollection {
    type Item = String;
    type IntoIter = RowIter;
    fn into_iter(self) -> Self::IntoIter {
        RowIter {
            items: self.0,
            index: 0,
        }
    }
}

/// Custom iterator: shared (borrowed) iteration.
pub struct SharedRows<'a> {
    items: &'a [String],
}

impl<'a> SharedRows<'a> {
    pub fn new(items: &'a [String]) -> Self {
        Self { items }
    }
}

impl<'a> IntoIterator for SharedRows<'a> {
    type Item = &'a String;
    type IntoIter = std::slice::Iter<'a, String>;
    fn into_iter(self) -> Self::IntoIter {
        self.items.iter()
    }
}

/// Custom iterator: mutable iteration.
pub struct MutRows<'a> {
    items: &'a mut Vec<String>,
}

impl<'a> MutRows<'a> {
    pub fn new(items: &'a mut Vec<String>) -> Self {
        Self { items }
    }
}

impl<'a> IntoIterator for MutRows<'a> {
    type Item = &'a mut String;
    type IntoIter = std::slice::IterMut<'a, String>;
    fn into_iter(self) -> Self::IntoIter {
        self.items.iter_mut()
    }
}

/// Value-returning loop via `break` value.
pub fn value_returning_loop(limit: i32) -> i32 {
    let result = loop {
        if limit > 0 {
            break 42;
        }
        break 0;
    };
    result
}

/// Nested labeled loops and blocks, with `continue` and label shadowing.
pub fn labeled_control() -> i32 {
    let mut outer_count: i32 = 0;
    let outer_result = 'outer: loop {
        'inner: loop {
            outer_count += 1;
            if outer_count == 2 {
                continue 'outer;
            }
            if outer_count >= 3 {
                break 'outer 99;
            }
            break 'inner;
        }
        if outer_count >= 3 {
            break 'outer outer_count;
        }
    };

    // Labeled block.
    let block_value = 'block: {
        if outer_count < 0 {
            break 'block 0;
        }
        outer_count + outer_result
    };

    // Label shadowing: inner label shadows outer reuse (compile-time allowed, distinct target).
    'shadow: loop {
        let _ = 'shadow: {
            break 'shadow 1_i32;
        };
        break;
    }

    block_value
}

/// `for` uses `IntoIterator` and repeated `next()` with defined temporary handling.
pub fn for_into_iterator() -> (usize, usize, usize) {
    let rows = vec!["plot".to_string(), "field".to_string(), "row".to_string()];

    // Owned IntoIterator.
    let owned_iter = RowCollection::new(rows.clone());
    let mut owned_count: usize = 0;
    for _item in owned_iter {
        owned_count += 1;
    }

    // Shared IntoIterator.
    let shared = SharedRows::new(&rows);
    let mut shared_count: usize = 0;
    for _item in shared {
        shared_count += 1;
    }

    // Mutable IntoIterator.
    let mut mutable_rows = rows.clone();
    let mut mut_count: usize = 0;
    for item in MutRows::new(&mut mutable_rows) {
        item.push_str("-ok");
        mut_count += 1;
    }

    (owned_count, shared_count, mut_count)
}

/// Demonstrates that temporary handling in `for` head is defined (array iteration edition sensitivity noted).
pub fn array_for_temporary() -> i32 {
    // Edition 2024/2021 array into_iter behavior is documented; array iteration uses IntoIterator for array.
    let arr = [1, 2, 3];
    let mut sum: i32 = 0;
    for val in arr {
        sum += val;
    }
    sum
}

/// Diverging loop as an intermediate: infinite loop only via break.
pub fn diverging_loop_background() -> i32 {
    let mut count: i32 = 0;
    loop {
        count += 1;
        if count == 5 {
            break count;
        }
    }
}

/// Closure control-boundary note: break/continue cannot cross closure boundary (valid: they target inner loop only).
pub fn closure_control_boundary() -> i32 {
    let mut sum: i32 = 0;
    let closure = || {
        // This loop is inside the closure; its break targets the closure-internal loop.
        let mut inner: i32 = 0;
        loop {
            inner += 1;
            if inner >= 3 {
                break inner;
            }
        }
    };
    sum += closure();
    sum
}

pub fn demonstrate() -> i32 {
    let _ = value_returning_loop(5);
    let _ = labeled_control();
    let _ = for_into_iterator();
    let _ = array_for_temporary();
    let _ = diverging_loop_background();
    let _ = closure_control_boundary();

    // Edition-sensitive array IntoIterator note: in 2021, `array.into_iter()` handling differs; documented but valid here.
    let _deque: VecDeque<i32> = VecDeque::from([1, 2, 3]);
    1
}
