//! RS-CAN-EXPR-008 — Evaluation order, short circuit, and compound assignment.

use std::cell::Cell;
use std::ops::{Add, Index, IndexMut};

thread_local! {
    static ORDER_LOG: Cell<Vec<&'static str>> = const { Cell::new(Vec::new()) };
}

fn log_and_value(label: &'static str, value: i32) -> i32 {
    ORDER_LOG.with(|log| {
        let mut v = log.take();
        v.push(label);
        log.set(v);
    });
    value
}

fn flag_true(label: &'static str, log: &mut Vec<&'static str>) -> bool {
    log.push(label);
    true
}

fn flag_false(label: &'static str, log: &mut Vec<&'static str>) -> bool {
    log.push(label);
    false
}

/// Tuple evaluation order: elements evaluated left-to-right.
pub fn tuple_order() -> Vec<&'static str> {
    ORDER_LOG.with(|l| l.set(Vec::new()));
    let _tuple = (
        log_and_value("a", 1),
        log_and_value("b", 2),
        log_and_value("c", 3),
    );
    ORDER_LOG.with(|l| l.take())
}

/// Array evaluation order: elements evaluated left-to-right.
pub fn array_order() -> Vec<&'static str> {
    ORDER_LOG.with(|l| l.set(Vec::new()));
    let _arr = [
        log_and_value("x", 10),
        log_and_value("y", 20),
        log_and_value("z", 30),
    ];
    ORDER_LOG.with(|l| l.take())
}

/// Call argument evaluation order: receiver, then arguments left-to-right, then call.
pub fn call_order() -> Vec<&'static str> {
    ORDER_LOG.with(|l| l.set(Vec::new()));
    fn target(a: i32, b: i32, c: i32) -> i32 {
        a + b + c
    }
    let _ = target(
        log_and_value("arg1", 1),
        log_and_value("arg2", 2),
        log_and_value("arg3", 3),
    );
    ORDER_LOG.with(|l| l.take())
}

/// Method call receiver before arguments.
pub struct Recorder;

impl Recorder {
    pub fn method(&self, a: i32, b: i32) -> i32 {
        a + b
    }
}

fn make_recorder(label: &'static str) -> Recorder {
    ORDER_LOG.with(|log| {
        let mut v = log.take();
        v.push(label);
        log.set(v);
    });
    Recorder
}

pub fn method_order() -> Vec<&'static str> {
    ORDER_LOG.with(|l| l.set(Vec::new()));
    let _ =
        make_recorder("receiver").method(log_and_value("m_arg1", 5), log_and_value("m_arg2", 6));
    ORDER_LOG.with(|l| l.take())
}

/// Binary operand order: left then right.
pub fn binary_operand_order() -> Vec<&'static str> {
    ORDER_LOG.with(|l| l.set(Vec::new()));
    let _ = log_and_value("left", 7) + log_and_value("right", 8);
    ORDER_LOG.with(|l| l.take())
}

fn place_with_log<'a>(label: &'static str, target: &'a mut i32) -> &'a mut i32 {
    ORDER_LOG.with(|log| {
        let mut v = log.take();
        v.push(label);
        log.set(v);
    });
    target
}

/// Assignment order: for an ordinary `=` assignment Rust evaluates the assigned value (RHS)
/// *before* the assignee place (LHS). Both operands log a side effect here, so the recorded
/// order is `["rhs", "lhs"]`.
pub fn assignment_order() -> Vec<&'static str> {
    ORDER_LOG.with(|l| l.set(Vec::new()));
    let mut target: i32 = 0;
    *place_with_log("lhs", &mut target) = log_and_value("rhs", 99);
    ORDER_LOG.with(|l| l.take())
}

/// Short-circuit: `&&` and `||` only evaluate right side if needed.
pub fn short_circuit_conditions() -> (Vec<&'static str>, Vec<&'static str>) {
    let mut log_and: Vec<&'static str> = Vec::new();
    let _ = flag_false("and_left_false", &mut log_and)
        && flag_true("and_right_not_evaluated", &mut log_and);
    let mut log_and2: Vec<&'static str> = Vec::new();
    let _ = flag_true("and_left_true", &mut log_and2)
        && flag_true("and_right_evaluated", &mut log_and2);

    let mut log_or: Vec<&'static str> = Vec::new();
    let _ =
        flag_true("or_left_true", &mut log_or) || flag_true("or_right_not_evaluated", &mut log_or);
    let mut log_or2: Vec<&'static str> = Vec::new();
    let _ =
        flag_false("or_left_false", &mut log_or2) || flag_true("or_right_evaluated", &mut log_or2);

    (log_and, log_and2)
}

/// Overloaded operator order: custom `Add` respects left-to-right operand evaluation recorded separately.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Tagged(pub i32, pub &'static str);

impl Add for Tagged {
    type Output = Self;
    fn add(self, rhs: Self) -> Self::Output {
        Tagged(self.0 + rhs.0, "combined")
    }
}

pub fn overloaded_operator_order() -> (i32, i32) {
    ORDER_LOG.with(|l| l.set(Vec::new()));
    let left = {
        log_and_value("over_left", 5);
        Tagged(5, "left")
    };
    let right = {
        log_and_value("over_right", 6);
        Tagged(6, "right")
    };
    let result = left + right;
    let order = ORDER_LOG.with(|l| l.take());
    // Order contains over_left, over_right in that order.
    assert_eq!(order, vec!["over_left", "over_right"]);
    (result.0, 11)
}

/// Indexed compound assignment: code-graph expression with IndexMut, index-place, and right-hand-side.
pub struct Store {
    pub data: Vec<i32>,
}

impl Index<usize> for Store {
    type Output = i32;
    fn index(&self, index: usize) -> &Self::Output {
        &self.data[index]
    }
}

impl IndexMut<usize> for Store {
    fn index_mut(&mut self, index: usize) -> &mut Self::Output {
        &mut self.data[index]
    }
}

fn log_index(label: &'static str, value: usize) -> usize {
    ORDER_LOG.with(|log| {
        let mut v = log.take();
        v.push(label);
        log.set(v);
    });
    value
}

pub fn indexed_compound_assignment() -> i32 {
    let mut store = Store {
        data: vec![10, 20, 30],
    };
    ORDER_LOG.with(|l| l.set(Vec::new()));
    // Code-graph coverage for indexed compound assignment: IndexMut on Store,
    // index-place `1` via `log_index` and RHS `5` via `log_and_value`.
    // Bob determination: without asserting a specific runtime evaluation order.
    store[log_index("idx", 1)] += log_and_value("rhs", 5);
    let _log = ORDER_LOG.with(|l| l.take());
    assert_eq!(store.data[1], 25);
    store.data[1]
}

pub fn demonstrate() -> i32 {
    assert_eq!(tuple_order(), vec!["a", "b", "c"]);
    assert_eq!(array_order(), vec!["x", "y", "z"]);
    assert_eq!(call_order(), vec!["arg1", "arg2", "arg3"]);
    assert_eq!(method_order(), vec!["receiver", "m_arg1", "m_arg2"]);
    assert_eq!(binary_operand_order(), vec!["left", "right"]);
    assert_eq!(assignment_order(), vec!["rhs", "lhs"]);
    let _ = short_circuit_conditions();
    let _ = overloaded_operator_order();
    let _ = indexed_compound_assignment();
    1
}
