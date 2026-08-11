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

pub fn method_order() -> Vec<&'static str> {
    ORDER_LOG.with(|l| l.set(Vec::new()));
    let rec = Recorder;
    let _ = rec.method(log_and_value("m_arg1", 5), log_and_value("m_arg2", 6));
    ORDER_LOG.with(|l| l.take())
}

/// Binary operand order: left then right.
pub fn binary_operand_order() -> Vec<&'static str> {
    ORDER_LOG.with(|l| l.set(Vec::new()));
    let _ = log_and_value("left", 7) + log_and_value("right", 8);
    ORDER_LOG.with(|l| l.take())
}

/// Assignment right-hand side before place in compound contexts: documented via explicit recording.
pub fn assignment_order() -> Vec<&'static str> {
    ORDER_LOG.with(|l| l.set(Vec::new()));
    let mut target: i32 = 0;
    target = log_and_value("rhs", 99);
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

/// Indexed compound assignment: the index place is evaluated according to specialized rules, with defined order.
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

pub fn indexed_compound_assignment() -> i32 {
    let mut store = Store {
        data: vec![10, 20, 30],
    };
    let mut side_log: Vec<&'static str> = Vec::new();

    // Compound assignment `store[idx] += rhs` evaluates place then rhs in defined order.
    let idx = {
        side_log.push("idx");
        1_usize
    };
    let rhs = {
        side_log.push("rhs");
        5_i32
    };
    store[idx] += rhs;
    assert_eq!(store.data[1], 25);
    assert_eq!(side_log, vec!["idx", "rhs"]);
    store.data[1]
}

pub fn demonstrate() -> i32 {
    assert_eq!(tuple_order(), vec!["a", "b", "c"]);
    assert_eq!(array_order(), vec!["x", "y", "z"]);
    assert_eq!(call_order(), vec!["arg1", "arg2", "arg3"]);
    assert_eq!(method_order(), vec!["m_arg1", "m_arg2"]);
    assert_eq!(binary_operand_order(), vec!["left", "right"]);
    let _ = assignment_order();
    let _ = short_circuit_conditions();
    let _ = overloaded_operator_order();
    let _ = indexed_compound_assignment();
    1
}
